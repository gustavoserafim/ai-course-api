from enum import Enum
from typing import Callable, List, Union
from pydantic import BaseModel


class MotorEnum(str, Enum):
    MOTOR_A = "motor_a"
    MOTOR_B = "motor_b"

class MotorAPromptMessage(BaseModel):
    role: str
    content: str

class PromptMotorA(BaseModel):
    max_new_tokens: int = 2000
    temperature: float = 0.1
    top_p: float = 0.95
    repetition_penalty: float = 1.2
    messages: List[MotorAPromptMessage]


class MotorBParameters(BaseModel):
    max_new_tokens: int = 2000
    temperature: float = 0.1

class PromptMotorB(BaseModel):
    inputs: str
    parameters: MotorBParameters

PROMPT_HANDLER_LIST = Union[
    PromptMotorA, 
    PromptMotorB
]

async def make_params_motor_a(prompt_text: str) -> PromptMotorA:
    prompt = MotorAPromptMessage(
        role="user",
        content=prompt_text)
    
    return PromptMotorA(messages=[prompt])

async def make_params_motor_b(prompt_text: str) -> PromptMotorB:
    return PromptMotorB(
        inputs=prompt_text,
        parameters=MotorBParameters()
    )

async def prompt_handler_factory(motor: MotorEnum) -> Callable:

    match motor:
        case MotorEnum.MOTOR_A:
            return make_params_motor_a
        case MotorEnum.MOTOR_B:
            return make_params_motor_b
        case _:
            raise ValueError(f"Invalid motor: {motor}")