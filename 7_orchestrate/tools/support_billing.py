import asyncio

from pydantic import BaseModel
from ibm_watsonx_orchestrate.flow_builder.flows import (
    END,
    Flow,
    flow,
    START,
    PromptNode,
)


use_case = "Billing Support"
subject_details = """Provide helpful, professional customer service responses for:
- Billing inquiries and invoice questions
- Payment issues and failed transactions
- Account charges and unexpected fees
- Refund requests and credit adjustments
- Payment method changes and updates
- Direct debit and automatic payment issues
- Billing disputes and corrections
- Account balance and payment history

Provide clear explanations, next steps, and reassurance."""


class Response(BaseModel):
    text: str


class Message(BaseModel):
    f"""
    This class represents the content of a support request for {use_case}.

    Attributes:
        message (str): Request text
    """
    message: str


def build_prompt_node(aflow: Flow) -> PromptNode:
    prompt_node = aflow.prompt(
        name="support_billing",
        display_name="Billing Support",
        description="This tool provides billing support responses for Deutsche Telekom customers.",
        system_prompt=f"""You are a helpful billing support expert for Deutsche Telekom.
Provide a direct, friendly, and professional response to the customer's billing inquiry.
Be empathetic about billing concerns and provide clear explanations.
Offer specific next steps and reassurance when appropriate.

{subject_details}

""",
        user_prompt="Customer inquiry: {message}",
        llm="meta-llama/llama-4-maverick-17b-128e-instruct-fp8",
        llm_parameters={
            "temperature": 0.3,
            "min_new_tokens": 50,
            "max_new_tokens": 1000,
            "top_k": None,
            "top_p": None,
            "stop_sequences": None,
        },
        input_schema=Message,
        output_schema=Response,
    )
    return prompt_node


@flow(name="support_billing", input_schema=Message, output_schema=Response)
def build_analysis_flow(aflow: Flow = None) -> Flow:
    """
    Creates a flow that will use the Prompt node to extract information from a customer email and returns an analysis.
    This flow will rely on the Flow engine to perform automatic data mapping at runtime.

    Args:
        aflow (Flow, optional): During deployment of the flow model, it will be passed a flow instance.

    Returns:
        Flow: The created flow.
    """
    prompt_node = build_prompt_node(aflow)

    aflow.sequence(START, prompt_node, END)

    return aflow


def on_flow_end(*args, **kwargs):
    print("on_flow_end")
    print(args)
    print(kwargs)


test_message = """Dear Deutsche Telekom,

I have received my monthly bill and there are several charges that I don't understand and believe are incorrect.

Issues with my bill:
- Extra charge of €29.99 for "Premium Services" - I never subscribed to this
- Roaming charges of €45.50 from last month - I was only in Austria for 2 days
- My monthly plan fee shows €39.99 but my contract states €34.99
- There's a "Service Fee" of €4.99 that wasn't mentioned in my contract

My account details:
- Customer number: 987654321
- Contract: MagentaMobil S
- Billing period: October 2024
- Invoice number: INV-2024-10-987654321

I have been a loyal customer for 5 years and have never had billing issues before. I would like these charges reviewed and corrected.

I have attached a copy of my original contract for reference.

Please investigate and provide a corrected bill.

Best regards,
Anna Schmidt
Phone: +49 151 12345678"""


async def main():

    my_flow_definition = build_analysis_flow()
    compiled_flow = await my_flow_definition.compile_deploy()
    await compiled_flow.invoke(
        {"message": test_message},
        on_flow_end_handler=on_flow_end,
        on_flow_error_handler=on_flow_end,
    )


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
