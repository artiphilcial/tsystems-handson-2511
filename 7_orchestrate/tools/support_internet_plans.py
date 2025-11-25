import asyncio

from pydantic import BaseModel
from ibm_watsonx_orchestrate.flow_builder.flows import (
    END,
    Flow,
    flow,
    START,
    PromptNode,
)


use_case = "Internet Plans Support"
subject_details = """Provide helpful, professional customer service responses for:
- Internet plan questions and comparisons
- Speed upgrades and downgrades
- Fiber optic availability and installation
- DSL vs Cable vs Fiber options
- Plan features and included services
- Contract terms and pricing
- Bundle options (internet + TV + phone)
- Installation and setup appointments

Provide clear plan comparisons, availability information, and recommendations."""


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
        name="support_internet_plans",
        display_name="Internet Plans Support",
        description="This tool provides internet plans support responses for Deutsche Telekom customers.",
        system_prompt=f"""You are a helpful internet plans expert for Deutsche Telekom.
Provide a direct, friendly, and professional response to the customer's internet plan inquiry.
Help them understand their options and make informed decisions about speed and features.
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


@flow(name="support_internet_plans", input_schema=Message, output_schema=Response)
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


test_message = """Hello Deutsche Telekom Team,

I am interested in upgrading my home internet connection and would like information about available options in my area.

Current situation:
- Current plan: MagentaZuhause M (50 Mbps DSL)
- Monthly cost: €34.99
- Address: Hauptstraße 45, 10115 Berlin
- Customer since: 2020
- Customer ID: 321654987

My requirements:
- Need faster internet for home office and streaming
- Family of 4 people, all using internet simultaneously
- Regular video conferencing for work
- 4K streaming on multiple devices
- Online gaming (son plays competitive games)
- Smart home devices (10+ connected devices)

Questions:
1. Is fiber optic available at my address?
2. What are the fastest speeds available for my location?
3. What is the price difference between 100 Mbps, 250 Mbps, and 500 Mbps plans?
4. Are there any bundle deals with TV services?
5. What is the installation process and timeline for fiber?
6. Can I keep my current phone number if I upgrade?
7. Are there any promotional offers for existing customers?
8. What is the minimum contract period for new plans?

Additional preferences:
- Prefer no long-term contract if possible
- Need reliable connection with minimal downtime
- Interested in MagentaTV if available
- Budget: up to €60/month for internet

Please provide detailed information about available plans and next steps.

Thank you,
Sarah Müller
Phone: +49 30 87654321
Email: s.mueller@email.com"""


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
