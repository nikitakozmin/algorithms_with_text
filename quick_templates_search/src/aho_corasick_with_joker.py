from collections import deque, defaultdict


class AhoCorasickNode:
    def __init__(self):
        self.transitions: dict[str, AhoCorasickNode] = {}
        self.suffix_link = None
        self.output = None
        self.offsets = []


def build_aho_corasick(patterns):
    root = AhoCorasickNode()
    
    for pattern, offset in patterns:
        node = root
        for c in pattern:
            if c not in node.transitions:
                node.transitions[c] = AhoCorasickNode()
            node = node.transitions[c]
        node.offsets.append(offset)
    
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
            child.output = child.suffix_link if child.suffix_link.offsets else child.suffix_link.output
    
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
            for offset in temp_node.offsets:
                sub = next(p for p, o in patterns if o == offset)
                sub_len = len(sub)
                start_pos = i - sub_len + 1
                occurrences.append((offset, start_pos))
            temp_node = temp_node.output
    
    return occurrences


def split_pattern(pattern, wildcard):
    subpatterns = []
    current_sub = []
    for i, c in enumerate(pattern):
        if c == wildcard:
            if current_sub:
                offset = i - len(current_sub)
                subpatterns.append((''.join(current_sub), offset))
                current_sub = []
        else:
            current_sub.append(c)
    if current_sub:
        offset = len(pattern) - len(current_sub)
        subpatterns.append((''.join(current_sub), offset))
    
    return subpatterns


def find_wildcard_matches(text, pattern, wildcard):
    subpatterns = split_pattern(pattern, wildcard)
    
    if not subpatterns:
        return []
    
    root = build_aho_corasick(subpatterns)
    sub_occurrences = search_aho_corasick(text, root, subpatterns)
    
    total_matches = set()
    len_pattern = len(pattern)
    len_text = len(text)
    
    offset_groups = defaultdict(list)
    for offset, start in sub_occurrences:
        offset_groups[offset].append(start)
    
    for offset, starts in offset_groups.items():
        
        for start in starts:
            full_start = start - offset
            if full_start < 1 or full_start + len_pattern - 1 > len_text:
                continue
            
            match = True
            for j in range(len_pattern):
                p_char = pattern[j]
                if p_char != wildcard and text[full_start - 1 + j] != p_char:
                    match = False
                    break
            
            if match:
                total_matches.add(full_start)
    
    return sorted(total_matches)


def main():
    text = input().strip()
    pattern = input().strip()
    joker = input().strip()
    
    matches = find_wildcard_matches(text, pattern, joker)
    for pos in matches:
        print(pos)


if __name__ == "__main__":
    main()
