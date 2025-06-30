import sys
from collections import deque


class AhoCorasickNode:
    def __init__(self):
        self.transitions: dict[str, AhoCorasickNode] = {}
        self.suffix_link = None
        self.output = None
        self.pattern_indices = []


def build_aho_corasick(patterns):
    root = AhoCorasickNode()
    
    for i, pattern in enumerate(patterns):
        node = root
        for c in pattern:
            if c not in node.transitions:
                node.transitions[c] = AhoCorasickNode()
            node = node.transitions[c]
        node.pattern_indices.append(i + 1)
    
    root.suffix_link = root
    queue = deque()
    for child in root.transitions.values():
        child.suffix_link = root
        queue.append(child)
    while queue:
        current_node: AhoCorasickNode = queue.popleft()
        for c, child in current_node.transitions.items():
            queue.append(child)
            suffix_node: AhoCorasickNode = current_node.suffix_link
            while suffix_node is not root and c not in suffix_node.transitions:
                suffix_node = suffix_node.suffix_link
            child.suffix_link = suffix_node.transitions.get(c, root)
            child.output = child.suffix_link if child.suffix_link.pattern_indices else child.suffix_link.output
    
    return root


def search_aho_corasick(text, root, patterns):
    occurrences = []
    current_node = root
    for i, c in enumerate(text, 1):
        while current_node is not root and c not in current_node.transitions:
            current_node: AhoCorasickNode = current_node.suffix_link
        if c in current_node.transitions:
            current_node = current_node.transitions[c]
        else:
            current_node = root
        
        temp_node = current_node
        while temp_node != None and temp_node is not root:
            for pattern_idx in temp_node.pattern_indices:
                pattern_length = len(patterns[pattern_idx - 1])
                start_pos = i - pattern_length + 1
                occurrences.append((start_pos, pattern_idx))
            temp_node = temp_node.output
    return occurrences


def main():
    input_lines = sys.stdin.read().splitlines()
    text = input_lines[0].strip()
    n_patterns = int(input_lines[1].strip())
    patterns = [line.strip() for line in input_lines[2:2 + n_patterns]]
    
    root = build_aho_corasick(patterns)
    occurrences = search_aho_corasick(text, root, patterns)
    
    occurrences.sort()
    for pos, pattern_idx in occurrences:
        print(pos, pattern_idx)

if __name__ == "__main__":
    main()
