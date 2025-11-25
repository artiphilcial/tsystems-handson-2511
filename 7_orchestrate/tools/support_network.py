import asyncio

from pydantic import BaseModel
from ibm_watsonx_orchestrate.flow_builder.flows import (
    END,
    Flow,
    flow,
    START,
    PromptNode,
)


use_case = "Network Support"
subject_details = """Provide helpful, professional customer service responses for:
- Internet connectivity issues and outages
- WiFi problems and signal strength issues
- Router and modem troubleshooting
- Network speed and performance problems
- Connection drops and instability
- DNS and IP configuration issues
- Network security concerns
- Fiber optic connection problems

Provide clear troubleshooting steps, explanations, and next actions."""


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
        name="support_network",
        display_name="Network Support",
        description="This tool provides network support responses for Deutsche Telekom customers.",
        system_prompt=f"""You are a helpful network support expert for Deutsche Telekom.
Provide a direct, friendly, and professional response to the customer's network-related inquiry.
Be concise but thorough. Offer clear troubleshooting steps when appropriate.
Show empathy for their issue and provide actionable solutions.

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


@flow(name="support_network", input_schema=Message, output_schema=Response)
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


test_message = """Dear Deutsche Telekom Support,

I am experiencing severe internet connectivity issues at my home address. The problem started yesterday evening and has been persistent.

Details of the issue:
- Internet connection keeps dropping every 10-15 minutes
- WiFi signal strength appears normal but no internet access
- Router lights show: Power (green), DSL (red), Internet (red)
- Speed when connected is much slower than usual (5 Mbps instead of 50 Mbps)
- Multiple devices affected (laptop, smartphone, smart TV)

I have already tried:
- Restarting the router multiple times
- Checking all cable connections
- Testing with ethernet cable directly

My contract details:
- Customer number: 123456789
- Plan: MagentaZuhause M (50 Mbps)
- Address: Musterstraße 123, 12345 Berlin

Please help resolve this issue as I work from home and need reliable internet.

Best regards,
Max Mustermann"""


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
