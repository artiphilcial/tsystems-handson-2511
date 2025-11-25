import asyncio

from pydantic import BaseModel
from ibm_watsonx_orchestrate.flow_builder.flows import (
    END,
    Flow,
    flow,
    START,
    PromptNode,
)


use_case = "Mobile Plans Support"
subject_details = """Provide helpful, professional customer service responses for:
- Mobile plan questions and comparisons
- Tariff changes and upgrades/downgrades
- Data allowances and usage monitoring
- Roaming charges and international plans
- Plan features and included services
- Contract terms and conditions
- Family plans and shared data
- Prepaid vs postpaid options

Provide clear plan comparisons, pricing information, and recommendations."""


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
        name="support_mobile_plans",
        display_name="Mobile Plans Support",
        description="This tool provides mobile plans support responses for Deutsche Telekom customers.",
        system_prompt=f"""You are a helpful mobile plans expert for Deutsche Telekom.
Provide a direct, friendly, and professional response to the customer's mobile plan inquiry.
Help them understand their options and make informed decisions.
Provide clear comparisons and recommendations based on their needs.

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


@flow(name="support_mobile_plans", input_schema=Message, output_schema=Response)
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

I would like to upgrade my current mobile plan as my data usage has increased significantly due to working from home.

Current situation:
- Current plan: MagentaMobil S (6GB data, unlimited calls/SMS)
- Monthly cost: €29.99
- Contract started: January 2023
- Phone number: +49 151 98765432
- Customer ID: 789123456

My needs:
- Need at least 15-20GB of data per month
- Currently using about 12-15GB monthly
- Frequently travel to EU countries for business
- Need good network coverage in rural areas
- Want to keep my current phone number

Questions:
1. What upgrade options are available for my current contract?
2. Can I upgrade without extending my contract period?
3. What are the costs for EU roaming with different plans?
4. Is there a family plan option? (My wife also needs a new plan)
5. Do you offer any discounts for long-term customers?

Additional information:
- I have been a Telekom customer for 8 years
- Currently using iPhone 13 Pro
- No issues with current service quality
- Prefer to keep monthly costs under €50 if possible

Please provide me with suitable plan options and pricing.

Best regards,
Michael Schneider
Email: m.schneider@email.com"""


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
