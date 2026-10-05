"""Ternary nodes for the brain coder.

Plan nodes have three children: left, mid, right.
Symbol lookup is a ternary search tree: lo, eq, hi on one character.
"""

from __future__ import annotations

from collections import deque
from typing import Any, Optional


class TernaryNode:
    __slots__ = ("value", "left", "mid", "right")

    def __init__(self, value: Any):
        self.value = value
        self.left: Optional[TernaryNode] = None
        self.mid: Optional[TernaryNode] = None
        self.right: Optional[TernaryNode] = None


class TernaryTree:
    def __init__(self) -> None:
        self.root: Optional[TernaryNode] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def insert(self, value: Any) -> None:
        node = TernaryNode(value)
        if self.root is None:
            self.root = node
            self._size = 1
            return
        queue = deque([self.root])
        while queue:
            cur = queue.popleft()
            for attr in ("left", "mid", "right"):
                child = getattr(cur, attr)
                if child is None:
                    setattr(cur, attr, node)
                    self._size += 1
                    return
                queue.append(child)

    def pretty(self) -> str:
        if self.root is None:
            return "<empty>"
        lines: list[str] = []

        def walk(n: Optional[TernaryNode], prefix: str, last: bool, label: str) -> None:
            if n is None:
                return
            lines.append(prefix + ("└── " if last else "├── ") + label + ":" + str(n.value))
            nxt = prefix + ("    " if last else "│   ")
            kids = [(n.left, "L"), (n.mid, "M"), (n.right, "R")]
            kids = [(c, lab) for c, lab in kids if c is not None]
            for i, (child, lab) in enumerate(kids):
                walk(child, nxt, i == len(kids) - 1, lab)

        walk(self.root, "", True, "root")
        return "\n".join(lines)


class TSTNode:
    __slots__ = ("char", "left", "mid", "right", "is_end", "value")

    def __init__(self, char: str):
        self.char = char
        self.left: Optional[TSTNode] = None
        self.mid: Optional[TSTNode] = None
        self.right: Optional[TSTNode] = None
        self.is_end = False
        self.value: Any = None


class TernarySearchTree:
    def __init__(self) -> None:
        self.root: Optional[TSTNode] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def insert(self, key: str, value: Any = True) -> None:
        if key:
            self.root = self._insert(self.root, key, 0, value)

    def _insert(self, node: Optional[TSTNode], key: str, idx: int, value: Any) -> TSTNode:
        char = key[idx]
        if node is None:
            node = TSTNode(char)
        if char < node.char:
            node.left = self._insert(node.left, key, idx, value)
        elif char > node.char:
            node.right = self._insert(node.right, key, idx, value)
        elif idx + 1 == len(key):
            if not node.is_end:
                self._size += 1
            node.is_end = True
            node.value = value
        else:
            node.mid = self._insert(node.mid, key, idx + 1, value)
        return node

    def get(self, key: str) -> Any:
        node = self._get(key)
        return node.value if node and node.is_end else None

    def _get(self, key: str) -> Optional[TSTNode]:
        node = self.root
        idx = 0
        while node is not None and idx < len(key):
            char = key[idx]
            if char < node.char:
                node = node.left
            elif char > node.char:
                node = node.right
            elif idx + 1 == len(key):
                return node
            else:
                node = node.mid
                idx += 1
        return None

    def starts_with(self, prefix: str) -> list[str]:
        out: list[str] = []
        if not prefix:
            self._collect(self.root, "", out)
            return out
        node = self._get(prefix)
        if node is None:
            return []
        if node.is_end:
            out.append(prefix)
        self._collect(node.mid, prefix, out)
        return out

    def _collect(self, node: Optional[TSTNode], prefix: str, out: list[str]) -> None:
        if node is None:
            return
        self._collect(node.left, prefix, out)
        if node.is_end:
            out.append(prefix + node.char)
        self._collect(node.mid, prefix + node.char, out)
        self._collect(node.right, prefix, out)
