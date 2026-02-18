from dotenv import load_dotenv
load_dotenv()

from pprint import pprint
from dataclasses import dataclass, field
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model
from langgraph.types import Command
from langchain.messages import HumanMessage, ToolMessage
from langchain.agents import AgentState
from langchain.agents.middleware import HumanInTheLoopMiddleware, dynamic_prompt, wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

# --------------- MODEL ---------------
model = init_chat_model(model="gpt-5-nano")

# --------------- CONTEXT ---------------
@dataclass
class LoginContext:
    users_db: dict = field(default_factory = lambda: {"user1@mail.com": "123",
                                                      "user2@mail.com": "321"})

# --------------- STATE ---------------
class AuthState(AgentState):
    authenticated: bool

# --------------- TOOLS ---------------
@tool
def check_inbox() -> str:
    """Check the inbox for recent emails"""
    return """
    Hi Julie,
    I'm going to be in town next week and was wondering if we could grab a coffee?
    - best, Jane (jane@example.com)
    """

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an response email"""
    return f"Email sent to {to} with subject {subject} and body {body}"

@tool
def authenticate(runtime: ToolRuntime, email: str, password: str):
    """Perform the user login based on the provided email and password"""
    if password_db := runtime.context.users_db.get(email):
        if password_db == password:
            return Command(update={
                "authenticated": True,
                "messages": [ToolMessage("Login Successful", tool_call_id=runtime.tool_call_id)]
            }
            )
    return Command(update={
        "authenticated": False,
        "messages": [ToolMessage("Login Failed", tool_call_id=runtime.tool_call_id)]
    }
    )

# --------------- MIDDLEWARE ---------------
@wrap_model_call
async def dynamic_tool_call(request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    """Allow read inbox and send email tools only if user provides correct email and password"""

    if  request.state.get("authenticated"):
        tools = [check_inbox, send_email]
    else:
        tools = [authenticate]
        request = request.override(tools=tools)
    return await handler(request)

authenticated_prompt = "You are a helpful assistant that can check the inbox and send emails."
unauthenticated_prompt = "You are a helpful assistant that can authenticate users."

@dynamic_prompt
def dynamic_prompt(request: ModelRequest) -> str:
    """Generate system prompt based on authentication status"""
    authenticated = request.state.get("authenticated")

    if authenticated:
        return authenticated_prompt
    else:
        return unauthenticated_prompt

hitl_middleware = HumanInTheLoopMiddleware(interrupt_on={
                            "authenticate": False,
                            "check_inbox": False,
                            "send_email": True,
                        }
                    )

# --------------- EMAIL AGENT ---------------
agent = create_agent(
    model=model,
    tools=[authenticate, check_inbox, send_email],
    state_schema=AuthState,
    context_schema=LoginContext,
    middleware=[dynamic_tool_call, dynamic_prompt, hitl_middleware]
)