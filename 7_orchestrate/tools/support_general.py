import asyncio

from pydantic import BaseModel
from ibm_watsonx_orchestrate.flow_builder.flows import (
    END,
    Flow,
    flow,
    START,
    PromptNode,
)


use_case = "General Support"
subject_details = """Provide helpful, professional customer service responses for:
- General account information and inquiries
- Contract questions and terms
- Service availability in specific areas
- Customer data updates (address, payment method, etc.)
- SIM card requests and replacements
- Customer identification and verification
- General product information
- Other inquiries not covered by specialized support areas

Provide clear information, next steps, and helpful guidance."""


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
        name="support_general",
        display_name="General Support",
        description="This tool provides general support responses for Deutsche Telekom customers.",
        system_prompt=f"""You are a helpful general support expert for Deutsche Telekom.
Provide a direct, friendly, and professional response to the customer's inquiry.
Be helpful and guide them through any processes or provide the information they need.
Offer clear next steps and assistance.

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


@flow(name="support_general", input_schema=Message, output_schema=Response)
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

I am moving to a new apartment next month and need to update my account information and transfer my services.

Current information:
- Customer ID: 147258369
- Current address: Berliner Straße 78, 20095 Hamburg
- Services: MagentaZuhause L (Internet) + MagentaMobil M
- Contract valid until: December 2025

New information:
- New address: Münchener Allee 123, 80331 München
- Moving date: December 15, 2024
- New apartment is in a newly built complex

My questions:
1. How do I transfer my internet service to the new address?
2. Is Deutsche Telekom service available at the new address?
3. Will I need a new router or can I use my current Speedport?
4. Can I keep my current phone number?
5. Are there any fees for the address change?
6. How long does the transfer process take?
7. Will there be any service interruption?
8. Do I need to schedule a technician visit?

Additional requests:
- Need to update my billing address
- Want to change payment method to direct debit
- Request a new SIM card (current one is damaged)
- Need confirmation letter for my new landlord

Please let me know the process and what documents I need to provide.

Best regards,
Julia Fischer
Current phone: +49 40 12345678
Email: j.fischer@email.com"""


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
