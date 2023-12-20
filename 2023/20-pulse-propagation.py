import abc
from enum import Enum
# import queue


class Pulse(Enum):
    LOW = 0
    HIGH = 1


class Module:
    def __init__(self, name, output_mods):
        self.name = name
        self.outputs, self.n_outs = output_mods, len(output_mods)
        self.low_count, self.high_count = 0, 0
        self.msg_q = []

    @abc.abstractmethod
    def receive(self):
        pass

    @abc.abstractmethod
    def send(self):
        pass

    def _update_pulse_count(self, pulse_sent):
        if pulse_sent == Pulse.LOW:
            self.low_count += self.n_outs
        elif pulse_sent == Pulse.HIGH:
            self.high_count += self.n_outs
        else:
            raise Exception("this should never be reached!")

    def __str__(self):
        return f"[{self.name}: {(self.low_count, self.high_count)}]"

    def __repr__(self):
        return self.__str__()


class FlipFlop(Module):
    def __init__(self, name, output_mods):
        super(FlipFlop, self).__init__(name, output_mods)
        self.state = 0

    def receive(self, src: str, pulse: Pulse):
        assert bool(src)
        self.msg_q.append((src, pulse))

    def send(self, module_registry, process_queue):
        _, received = self.msg_q.pop(0)
        # print(f"{self.name} received {received} from {src}")
        if received == Pulse.LOW:
            pulse_to_send = Pulse.LOW if self.state else Pulse.HIGH
            self.state = int(not self.state)
            for mod_id in self.outputs:
                mod_obj = module_registry[mod_id]
                mod_obj.receive(self.name, pulse_to_send)
                # print(f"{self.name} sent {pulse_to_send} to {mod_id}")
                process_queue.append(mod_obj)
            self._update_pulse_count(pulse_to_send)


class Conjuction(Module):
    def __init__(self, name, output_mods, input_mods):
        super(Conjuction, self).__init__(name, output_mods)
        self.memory = {im: Pulse.LOW for im in input_mods}

    def receive(self, src: str, pulse: Pulse):
        self.msg_q.append((src, pulse))

    def send(self, module_registry, process_queue):
        src, received = self.msg_q.pop(0)
        self.memory[src] = received
        pulse_to_send = Pulse.LOW if all(p == Pulse.HIGH for p in self.memory.values()) else Pulse.HIGH
        # print(f"{self.name} has memory {self.memory}, {len(self.memory)}")
        for mod_id in self.outputs:
            mod_obj = module_registry[mod_id]
            mod_obj.receive(self.name, pulse_to_send)
            # print(f"{self.name} sent {pulse_to_send} to {mod_id}")
            process_queue.append(mod_obj)
        self._update_pulse_count(pulse_to_send)


class Broadcaster(Module):
    def __init__(self, name, output_mods):
        super(Broadcaster, self).__init__(name, output_mods)

    def receive(self, src: str, pulse: Pulse):
        assert src == "button" and pulse == Pulse.LOW
        self.msg_q.append((src, pulse))

    def send(self, module_registry, process_queue):
        _, pulse_to_send = self.msg_q.pop(0)
        for mod_id in self.outputs:
            mod_obj = module_registry[mod_id]
            mod_obj.receive(self.name, pulse_to_send)
            # print(f"{self.name} sent {pulse_to_send} to {mod_id}")
            process_queue.append(mod_obj)
        self._update_pulse_count(pulse_to_send)


def init_and_get_module(mod_id, outputs_ls, conjunction_inputs):
    if mod_id == "broadcaster":
        mod_name = mod_id
        return mod_name, Broadcaster(mod_name, outputs_ls)
    elif mod_id.startswith("%"):
        mod_name = mod_id[1:]
        return mod_name, FlipFlop(mod_name, outputs_ls)
    elif mod_id.startswith("&"):
        mod_name = mod_id[1:]
        return mod_name, Conjuction(mod_name, outputs_ls, conjunction_inputs[mod_name])
    else:
        raise Exception("this should never be reached!")


def get_mod_conns(data):
    return {mod_id.strip(): [dst.strip() for dst in outputs.split(',')] 
        for mod_id, outputs in [line.strip().split('->') for line in data.splitlines()]}


def get_conjunction_inputs(mod_conns_map):
    conjuction_inputs = {}
    for conj_name in {mod_name[1:] for mod_name in mod_conns_map.keys() if mod_name.startswith("&")}:
        conjuction_inputs[conj_name] = []
        for mod_name, outputs_ls in mod_conns_map.items():
            if conj_name in outputs_ls:
                assert mod_name.startswith("%") or mod_name.startswith("&")
                conjuction_inputs[conj_name].append(mod_name[1:])
    return conjuction_inputs


def create_module_registry(data):
    mod_conns_map = get_mod_conns(data)
    conjunction_inputs = get_conjunction_inputs(mod_conns_map)

    return {mod_name: mod_obj for mod_name, mod_obj in
        (init_and_get_module(mod_name, outputs, conjunction_inputs)
        for mod_name, outputs in mod_conns_map.items())}


def signal_system(mod_reg, button_presses):
    pq = []
    for _ in range(button_presses):
        init_mod = mod_reg["broadcaster"]
        init_mod.receive("button", Pulse.LOW)
        pq.append(init_mod)

        # print()
        # print(pq)
        # for mod in mod_reg.values():
        #     print(mod, end="\t")
        # print()
        while pq:
            curr_mod = pq.pop(0)
            curr_mod.send(mod_reg, pq)

            # print()
            # print(pq)
            # for mod in mod_reg.values():
            #     print(mod, end="\t")
            # print()


def calc_total_signals(module_registry, button_count):
    low, high = button_count, 0
    for _, mod_obj in module_registry.items():
        low += mod_obj.low_count
        high += mod_obj.high_count

    return low, high, low * high


if __name__ == "__main__":
    with open("../inputs/2023/20.txt") as f:
        data = f.read().strip()

    example_1 = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
    """

    example_2 = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
    """

    # data = example_1.strip()
    # data = example_2.strip()

    mod_reg = create_module_registry(data)
    # print(mod_reg)

    # part 1
    mod_reg['rx'] = FlipFlop('rx', [])
    button_presses = 1000
    signal_system(mod_reg, button_presses)
    ans = calc_total_signals(mod_reg, button_presses)
    print(ans)
