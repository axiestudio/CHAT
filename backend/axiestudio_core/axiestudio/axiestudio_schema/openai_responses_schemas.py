from typing import Any, Literal

from pydantic import BaseModel, Field


class OpenAIMessage(BaseModel):
    """OpenAI message format."""
    role: Literal["system", "user", "assistant"] = Field(..., description="The role of the message author")
    content: str = Field(..., description="The content of the message")


class OpenAIResponsesRequest(BaseModel):
    """OpenAI-compatible chat completions request with flow_id as model parameter."""

    model: str = Field(..., description="The flow ID to execute (used instead of OpenAI model)")
    messages: list[OpenAIMessage] = Field(..., description="List of messages in the conversation")
    stream: bool = Field(default=False, description="Whether to stream the response")
    temperature: float = Field(default=1.0, description="Sampling temperature")
    max_tokens: int | None = Field(default=None, description="Maximum number of tokens to generate")
    top_p: float = Field(default=1.0, description="Nucleus sampling parameter")
    frequency_penalty: float = Field(default=0.0, description="Frequency penalty")
    presence_penalty: float = Field(default=0.0, description="Presence penalty")
    stop: str | list[str] | None = Field(default=None, description="Stop sequences")
    user: str | None = Field(default=None, description="User identifier")
    session_id: str | None = Field(default=None, description="Session identifier for conversation continuity")
    tweaks: dict[str, Any] | None = Field(default=None, description="Flow-specific tweaks/parameters")


class OpenAIChoice(BaseModel):
    """OpenAI choice format."""
    index: int = Field(..., description="The index of the choice")
    message: dict[str, Any] = Field(..., description="The message content")
    finish_reason: str | None = Field(..., description="The reason the generation finished")


class OpenAIUsage(BaseModel):
    """OpenAI usage statistics."""
    prompt_tokens: int = Field(..., description="Number of tokens in the prompt")
    completion_tokens: int = Field(..., description="Number of tokens in the completion")
    total_tokens: int = Field(..., description="Total number of tokens")


class OpenAIResponsesResponse(BaseModel):
    """OpenAI-compatible chat completions response."""

    id: str = Field(..., description="Unique identifier for the completion")
    object: Literal["chat.completion"] = "chat.completion"
    created: int = Field(..., description="Unix timestamp of creation")
    model: str = Field(..., description="The model (flow) used")
    choices: list[dict[str, Any]] = Field(..., description="List of completion choices")
    usage: dict[str, Any] | None = Field(default=None, description="Token usage statistics")
    system_fingerprint: str | None = Field(default=None, description="System fingerprint")


class OpenAIStreamChoice(BaseModel):
    """OpenAI streaming choice format."""
    index: int = Field(..., description="The index of the choice")
    delta: dict[str, Any] = Field(..., description="The delta content")
    finish_reason: str | None = Field(default=None, description="The reason the generation finished")


class OpenAIResponsesStreamChunk(BaseModel):
    """OpenAI-compatible streaming response chunk."""

    id: str = Field(..., description="Unique identifier for the completion")
    object: Literal["chat.completion.chunk"] = "chat.completion.chunk"
    created: int = Field(..., description="Unix timestamp of creation")
    model: str = Field(..., description="The model (flow) used")
    choices: list[dict[str, Any]] = Field(..., description="List of streaming choices")
    system_fingerprint: str | None = Field(default=None, description="System fingerprint")


class OpenAIErrorResponse(BaseModel):
    """OpenAI-compatible error response."""
    error: dict[str, Any] = Field(..., description="Error details")


def create_openai_error(message: str, type_: str = "invalid_request_error", code: str | None = None) -> dict:
    """Create an OpenAI-compatible error response."""
    error_data = {
        "message": message,
        "type": type_,
        "param": None,
        "code": code,
    }

    return {"error": error_data}
