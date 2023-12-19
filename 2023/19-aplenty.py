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
