from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional

RoleType = Literal["system", "user", "assistant", "environment"]

@dataclass(frozen=True)
class ChatMessage:
    role: RoleType
    content: str
    name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {"role": self.role, "content": self.content}

        if self.name:
            result["name"] = self.name

        return result

@dataclass
class ChatConversation:
    messages: List[ChatMessage] = field(default_factory=list)

    def add_system_message(self, content: str) -> None:
        self._add_message(role="system", content=content, name=None, metadata=None)

    def add_user_message(self, content: str, name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> None:
        self._add_message(role="user", content=content, name=name, metadata=metadata)

    def add_assistant_message(self, content: str) -> None:
        self._add_message(role="assistant", content=content, name=None, metadata=None)

    def add_environment_message(self, content: str) -> None:
        self._add_message(role="environment", content=content, name=None, metadata=None)

    def _add_message(
        self,
        role: RoleType,
        content: str,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.messages.append(
            ChatMessage(
                role=role,
                content=content,
                name=name,
                metadata=metadata,
            )
        )

    
    def to_openai_format(self) -> list:
        return [message.to_dict() for message in self.messages]

