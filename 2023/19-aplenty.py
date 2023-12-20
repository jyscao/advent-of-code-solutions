def make_rule_judger(rules_ls):
    def rule_judger(part):
        R = len(rules_ls)
        for i, rule in enumerate(rules_ls, start=1):
            if ':' in rule:
                cond, dest = rule.strip().split(':')
                if '<' in cond:
                    attr, threshold = cond.strip().split('<')
                    if part[attr] < int(threshold):
                        return dest
                elif '>' in cond:
                    attr, threshold = cond.strip().split('>')
                    if part[attr] > int(threshold):
                        return dest
            else:
                assert i == R
                return rule.strip()
    return rule_judger


def extract_workflow(wfs):
    return {wid: make_rule_judger([r for r in rules.strip('} ').split(',')])
        for wid, rules in (wf.split('{') for wf in wfs.strip().splitlines())}


def get_parts_list(parts):
    return [{k: int(v) for k, v in (tuple(atup.split('=')) for atup in p.strip('{} ').split(','))}
        for p in parts.strip().splitlines()]


def process_parts(wfs, parts):
    workflow = extract_workflow(wfs)
    parts_ls = get_parts_list(parts)

    accepted = []
    for part in parts_ls:
        dest = "in"
        while dest not in {"A", "R"}:
            dest = workflow[dest](part)
            if dest == "A":
                accepted.append(part)

    return sum(sum(v for v in part.values()) for part in accepted)


def build_wf_tree(wfs):
    workflows_map = {wid: rules_str.strip('} ') for wid, rules_str in 
        (wf.split('{') for wf in wfs.strip().splitlines())}

    class WorkflowNode:
        def __init__(self, label, condition=(), left=None, right=None, allowed_parts={}):
            self.label = label
            self.condition = condition
            self.left = left
            self.right = right
            self.allowed_parts = allowed_parts

        def build_tree_str(self, parent_prefix, show_parts_range=True, extra_line_space=False):
            if self.label in ("A", "R",):
                label = {"A": "Accept", "R": "Reject"}[self.label]
                ap_str = f" ⟶ {self.allowed_parts}" if show_parts_range else ""
                str_rep = f"<{label}>{ap_str}"
            else:
                label = f"{self.label} | " if self.label else ""
                ap_str = f" ⟶ {self.allowed_parts}" if show_parts_range else ""
                condition = f"{' '.join(str(v) for v in self.condition)}" if self.condition else ""
                str_rep = f"{'{ '}{label}{condition}{' }'}{ap_str}"

            if self.left and self.right:
                if self.left.label == self.right.label:
                    result_label = {"A": "Accept", "R": "Reject"}[self.left.label]
                    str_rep += f" ⟵ <{result_label}>"
                else:
                    prefix_l, prefix_r = f"{parent_prefix}\t┣━━━━", f"{parent_prefix}\t┗━━━━"
                    prefix_child_l, prefix_child_r = f"{parent_prefix}\t┃", f"{parent_prefix}\t"

                    extra_line_space = f"\n{prefix_child_l}" if extra_line_space else ""
                    str_rep += extra_line_space + "\n" + prefix_l + WorkflowNode.build_tree_str(self.left, prefix_child_l)
                    str_rep += extra_line_space + "\n" + prefix_r + WorkflowNode.build_tree_str(self.right, prefix_child_r)
            return str_rep

        def __str__(self):
            return self.build_tree_str("")


    def parse_cond(cond_dest):
        if ":" in cond_dest:
            cond, dest = cond_dest.split(':')
            if '<' in cond:
                attr, threshold = cond.strip().split('<')
                return (attr, '<', int(threshold)), dest
            elif '>' in cond:
                attr, threshold = cond.strip().split('>')
                return (attr, '>', int(threshold)), dest
            else:
                raise Exception("this should never be reached")
        else:
            return None, cond_dest

    def build_from_node(identifier):
        if identifier in ("A", "R",):
            return WorkflowNode(identifier)

        if identifier in workflows_map:
            wid, rule = identifier, workflows_map[identifier]
        else:
            wid, rule = "", identifier

        try:
            cond, rest = rule.split(',', maxsplit=1)
        except ValueError:
            assert ":" not in rule
            cond, rest = rule, None

        wfnode = WorkflowNode(wid)
        condition, dest = parse_cond(cond)
        if condition:
            wfnode.condition = condition
        wfnode.left = build_from_node(dest)
        wfnode.right = build_from_node(rest)
        return wfnode

    return build_from_node("in")


def calc_total_acceptable(wf_tree, attr_max=4000):
    import copy
    wf_tree.allowed_parts = {attr: (1, attr_max) for attr in 'xmas'}

    def traverse_wf_tree_get_total(node):
        if node.label == "A":
            res = 1
            for a, b in node.allowed_parts.values():
                res *= b - a + 1
            return res
        elif node.label == "R":
            return 0

        attr, comparison, threshold = node.condition
        unfiltered = node.allowed_parts
        if comparison == "<":
            filtered_l, filtered_r = copy.copy(unfiltered), copy.copy(unfiltered)
            a, b = unfiltered[attr]
            filtered_l[attr] = (a, threshold - 1)
            filtered_r[attr] = (threshold, b)
        elif comparison == ">":
            filtered_l, filtered_r = copy.copy(unfiltered), copy.copy(unfiltered)
            a, b = unfiltered[attr]
            filtered_l[attr] = (threshold + 1, b)
            filtered_r[attr] = (a, threshold)
        else:
            raise Exception("this should never be reached!")

        node.left.allowed_parts = filtered_l
        node.right.allowed_parts = filtered_r

        return traverse_wf_tree_get_total(node.left) + traverse_wf_tree_get_total(node.right)

    return traverse_wf_tree_get_total(wf_tree)



if __name__ == "__main__":
    with open("../inputs/2023/19.txt") as f:
        wfs, parts = f.read().strip().split("\n\n")

    test_data = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
    """
    wfs, parts = test_data.strip().split("\n\n")

    # part 1
    res = process_parts(wfs, parts)
    print(res)

    # part 2
    wf_tree = build_wf_tree(wfs)
    total_acceptable = calc_total_acceptable(wf_tree)
    print(total_acceptable)
    print(wf_tree)
