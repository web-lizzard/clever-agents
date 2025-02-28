from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any, Union


class RoleType(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    ENVIRONMENT = "environment"


@dataclass(frozen=True)
class ChatMessage:
    role: RoleType
    content: str
    name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {"role": self.role.value, "content": self.content}

        if self.name:
            result["name"] = self.name

        return result


@dataclass
class ChatMLDocument:
    messages: List[ChatMessage] = field(default_factory=list)

    def add_message(
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

    def to_list(self) -> list:
        return [message.to_dict() for message in self.messages]
