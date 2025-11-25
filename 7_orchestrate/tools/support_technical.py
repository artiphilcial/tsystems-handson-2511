import asyncio

from pydantic import BaseModel
from ibm_watsonx_orchestrate.flow_builder.flows import (
    END,
    Flow,
    flow,
    START,
    PromptNode,
)


use_case = "Technical Support"
subject_details = """Provide helpful, professional customer service responses for:
- Device configuration and setup issues
- Router and modem technical problems
- Software and firmware updates
- Email and app configuration
- Device compatibility issues
- Hardware troubleshooting
- Performance optimization
- Security settings and configurations

Provide step-by-step instructions and technical guidance."""


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
        name="support_technical",
        display_name="Technical Support",
        description="This tool provides technical support responses for Deutsche Telekom customers.",
        system_prompt=f"""You are a helpful technical support expert for Deutsche Telekom.
Provide a direct, friendly, and professional response to the customer's technical inquiry.
Offer clear, step-by-step troubleshooting instructions when appropriate.
Be patient and explain technical concepts in simple terms.

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


@flow(name="support_technical", input_schema=Message, output_schema=Response)
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


test_message = """Hello Deutsche Telekom Support,

I need help configuring my new Speedport Smart 4 router. I received it yesterday but I'm having several technical issues.

Problems I'm experiencing:
- Cannot access the router admin panel (192.168.1.1 doesn't work)
- WiFi network is not showing up on my devices
- The router keeps restarting every few minutes
- LED indicators: Power (green), DSL (blinking red), WiFi (off)
- Cannot complete the initial setup wizard

My setup:
- Router model: Speedport Smart 4
- Connection type: VDSL
- Previous router: Speedport W724V (worked fine)
- Operating system: Windows 11, macOS Monterey
- Devices: 2 laptops, 3 smartphones, 1 smart TV

What I've tried:
- Factory reset (holding reset button for 30 seconds)
- Different ethernet cables
- Connecting directly to laptop via ethernet
- Checking all cable connections
- Waiting 24 hours for line activation

My contract details:
- Customer ID: 456789123
- Plan: MagentaZuhause L
- Installation date: Yesterday (November 19, 2024)

I work from home and urgently need internet access. Please provide step-by-step configuration instructions.

Thank you,
Thomas Weber
Phone: +49 30 12345678"""


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
