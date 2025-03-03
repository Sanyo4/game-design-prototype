import random
import time
import os
import math
from enum import Enum
import sys
import curses
from collections import defaultdict


class OrderState(Enum):
    SUPERPOSITION = "SUPERPOSITION"
    COLLAPSED = "COLLAPSED"
    FAILED = "FAILED"
    DELIVERED = "DELIVERED"


class ResourceType(Enum):
    QUANTUM_ENERGY = "Quantum Energy"
    PROBABILITY_STABILIZER = "Probability Stabilizer"
    TIMELINE_TOKEN = "Timeline Token"


class DishType(Enum):
    QUANTUM_BURGER = "Quantum Burger"
    SCHRODINGER_SALAD = "Schrödinger's Salad"
    ENTANGLED_PASTA = "Entangled Pasta"
    PROBABILITY_PIE = "Probability Pie"
    WAVE_FUNCTION_SOUP = "Wave Function Soup"
    UNCERTAINTY_SUSHI = "Uncertainty Sushi"
    QUBIT_QUESADILLA = "Qubit Quesadilla"
    SUPERPOSITION_STIR_FRY = "Superposition Stir Fry"


class TimelineEvent(Enum):
    RESOURCE_BOOST = "Resource Boost"
    TIMELINE_SHIFT = "Timeline Shift"
    QUANTUM_FLUCTUATION = "Quantum Fluctuation"
    REALITY_DISTORTION = "Reality Distortion"


class MiniPuzzleType(Enum):
    SEQUENCE = "Sequence Puzzle"
    PATTERN = "Pattern Matching"
    PROBABILITY = "Probability Calculation"
    QUANTUM_STATE = "Quantum State Manipulation"


class Order:
    def __init__(self, day):
        self.id = random.randint(1000, 9999)
        self.state = OrderState.SUPERPOSITION
        self.dish = random.choice(list(DishType))
        self.time_limit = random.randint(3, 5 + min(day // 2, 5))
        self.time_remaining = self.time_limit
        self.difficulty = min(1 + day // 3, 5)
        self.resource_requirements = {
            ResourceType.QUANTUM_ENERGY: random.randint(1, 1 + self.difficulty),
            ResourceType.PROBABILITY_STABILIZER: random.randint(0, self.difficulty // 2),
            ResourceType.TIMELINE_TOKEN: random.randint(0, 1 if self.difficulty > 2 else 0)
        }
        self.reward = sum(self.resource_requirements.values()) * 10 + self.difficulty * 5
        self.puzzle = random.choice(list(MiniPuzzleType))
        self.possible_outcomes = self.generate_possible_outcomes()
        self.actual_outcome = None
        self.timeline = random.randint(1, min(2 + day // 3, 5))

    def generate_possible_outcomes(self):
        # Generate 2-4 possible outcomes for the order
        outcomes = []
        num_outcomes = random.randint(2, 4)

        # One perfect outcome
        perfect = {
            "description": f"Perfect {self.dish.value}",
            "satisfaction": 100,
            "reward_multiplier": 1.5,
            "probability": 0.2 + (0.1 * self.difficulty)  # Higher difficulty increases perfect probability
        }
        outcomes.append(perfect)

        # One good outcome
        good = {
            "description": f"Good {self.dish.value}",
            "satisfaction": 80,
            "reward_multiplier": 1.0,
            "probability": 0.4
        }
        outcomes.append(good)

        # Possibly a mediocre outcome
        if num_outcomes > 2:
            mediocre = {
                "description": f"Mediocre {self.dish.value}",
                "satisfaction": 50,
                "reward_multiplier": 0.7,
                "probability": 0.3
            }
            outcomes.append(mediocre)

        # Possibly a poor outcome
        if num_outcomes > 3:
            poor = {
                "description": f"Poor {self.dish.value}",
                "satisfaction": 20,
                "reward_multiplier": 0.3,
                "probability": 0.1
            }
            outcomes.append(poor)

        # Normalize probabilities
        total_prob = sum(outcome["probability"] for outcome in outcomes)
        for outcome in outcomes:
            outcome["probability"] /= total_prob

        return outcomes

    def collapse_state(self, bonus_probability=0):
        # Collapse the quantum state into a definite outcome
        if self.state != OrderState.SUPERPOSITION:
            return

        # Modified probabilities based on bonus
        modified_outcomes = self.possible_outcomes.copy()
        if bonus_probability > 0:
            # Increase probability of better outcomes
            for outcome in modified_outcomes:
                if outcome["satisfaction"] >= 80:
                    outcome["probability"] += bonus_probability
                else:
                    outcome["probability"] -= bonus_probability / (len(modified_outcomes) - 2)

            # Re-normalize
            total_prob = sum(outcome["probability"] for outcome in modified_outcomes)
            for outcome in modified_outcomes:
                outcome["probability"] /= total_prob

        # Select outcome based on probabilities
        rand = random.random()
        cumulative_prob = 0
        for outcome in modified_outcomes:
            cumulative_prob += outcome["probability"]
            if rand <= cumulative_prob:
                self.actual_outcome = outcome
                break

        self.state = OrderState.COLLAPSED

    def update_time(self):
        self.time_remaining -= 1
        if self.time_remaining <= 0 and self.state == OrderState.SUPERPOSITION:
            self.state = OrderState.FAILED
            return True
        return False

    def __str__(self):
        status = f"Order #{self.id}: {self.dish.value} - {self.state.value}"
        if self.state == OrderState.SUPERPOSITION:
            status += f" (Time: {self.time_remaining}/{self.time_limit}, Timeline: {self.timeline})"
        elif self.state == OrderState.COLLAPSED:
            status += f" - {self.actual_outcome['description']} (Satisfaction: {self.actual_outcome['satisfaction']}%)"
        return status

    def get_details(self):
        details = [
            f"Order #{self.id}: {self.dish.value}",
            f"State: {self.state.value}",
            f"Timeline: {self.timeline}",
            f"Time Remaining: {self.time_remaining}/{self.time_limit}",
            f"Difficulty: {self.difficulty} stars",
            f"Puzzle Type: {self.puzzle.value}",
            "Resource Requirements:"
        ]

        for resource, amount in self.resource_requirements.items():
            if amount > 0:
                details.append(f"  - {resource.value}: {amount}")

        details.append(f"Base Reward: {self.reward} points")

        if self.state == OrderState.SUPERPOSITION:
            details.append("\nPossible Outcomes:")
            for outcome in self.possible_outcomes:
                details.append(
                    f"  - {outcome['description']} (Satisfaction: {outcome['satisfaction']}%, Probability: {outcome['probability']:.1%})")
        elif self.state == OrderState.COLLAPSED:
            details.append(f"\nOutcome: {self.actual_outcome['description']}")
            details.append(f"Satisfaction: {self.actual_outcome['satisfaction']}%")
            details.append(f"Reward Multiplier: {self.actual_outcome['reward_multiplier']}x")

        return "\n".join(details)


class MiniPuzzle:
    def __init__(self, order):
        self.type = order.puzzle
        self.difficulty = order.difficulty
        self.order = order
        self.setup_puzzle()

    def setup_puzzle(self):
        if self.type == MiniPuzzleType.SEQUENCE:
            length = 3 + self.difficulty
            self.sequence = [random.randint(1, 9) for _ in range(length)]
            self.solution = self.sequence.copy()
            # Remove some numbers
            removals = min(length - 2, self.difficulty + 1)
            for _ in range(removals):
                idx = random.randint(0, len(self.sequence) - 1)
                while self.sequence[idx] is None:
                    idx = random.randint(0, len(self.sequence) - 1)
                self.sequence[idx] = None

        elif self.type == MiniPuzzleType.PATTERN:
            patterns = [
                ["#", ".", "#", "."],
                ["O", "X", "O", "X"],
                ["^", "v", "<", ">"],
                ["1", "0", "1", "0"]
            ]
            self.pattern = random.choice(patterns)
            length = 4 + self.difficulty * 2
            self.sequence = []

            # Generate a sequence with a pattern
            while len(self.sequence) < length:
                self.sequence.extend(self.pattern)
            self.sequence = self.sequence[:length]

            # Store the solution
            self.solution = self.sequence.copy()

            # Remove some elements
            removals = min(length - 4, self.difficulty * 2)
            for _ in range(removals):
                idx = random.randint(0, len(self.sequence) - 1)
                while self.sequence[idx] is None:
                    idx = random.randint(0, len(self.sequence) - 1)
                self.sequence[idx] = None

        elif self.type == MiniPuzzleType.PROBABILITY:
            # For probability calculation, we'll give a simple word problem
            dice_sides = random.randint(2, 6)
            target_value = random.randint(1, dice_sides)

            self.question = f"If a {dice_sides}-sided die is rolled, what's the probability of getting a {target_value}?"
            self.answer = f"1/{dice_sides}"
            self.solution = self.answer

        elif self.type == MiniPuzzleType.QUANTUM_STATE:
            # Simplified representation of quantum states |0⟩ and |1⟩
            states = ["|0⟩", "|1⟩", "|+⟩", "|-⟩"]
            operations = ["X", "Z", "H"]

            # Generate a sequence of operations
            num_operations = 1 + self.difficulty // 2
            self.initial_state = random.choice(states)
            self.operations = [random.choice(operations) for _ in range(num_operations)]

            # Determine the final state (simplified)
            if self.initial_state == "|0⟩":
                final_state = "|0⟩"
                for op in self.operations:
                    if op == "X":
                        final_state = "|1⟩" if final_state == "|0⟩" else "|0⟩"
                    elif op == "H":
                        final_state = "|+⟩" if final_state == "|0⟩" else "|-⟩"
            elif self.initial_state == "|1⟩":
                final_state = "|1⟩"
                for op in self.operations:
                    if op == "X":
                        final_state = "|0⟩" if final_state == "|1⟩" else "|1⟩"
                    elif op == "H":
                        final_state = "|-⟩" if final_state == "|1⟩" else "|+⟩"
            else:
                # For simplified puzzles, just alternate between |+⟩ and |-⟩
                final_state = "|+⟩" if len(self.operations) % 2 == 0 else "|-⟩"

            self.question = f"If we start with {self.initial_state} and apply the operations {' '.join(self.operations)}, what's the final state?"
            self.answer = final_state
            self.solution = self.answer

    def get_puzzle_description(self):
        if self.type == MiniPuzzleType.SEQUENCE:
            description = "Complete the sequence by filling in the missing numbers:\n"
            sequence_str = []
            for i, num in enumerate(self.sequence):
                if num is None:
                    sequence_str.append("_")
                else:
                    sequence_str.append(str(num))
            description += " ".join(sequence_str)

        elif self.type == MiniPuzzleType.PATTERN:
            description = "Complete the pattern by filling in the missing symbols:\n"
            pattern_str = []
            for i, sym in enumerate(self.sequence):
                if sym is None:
                    pattern_str.append("_")
                else:
                    pattern_str.append(sym)
            description += " ".join(pattern_str)

        elif self.type == MiniPuzzleType.PROBABILITY:
            description = self.question

        elif self.type == MiniPuzzleType.QUANTUM_STATE:
            description = self.question

        return description

    def check_solution(self, user_answer):
        if self.type == MiniPuzzleType.SEQUENCE or self.type == MiniPuzzleType.PATTERN:
            # For sequence/pattern, user_answer should be a list of answers to fill in
            if len(user_answer) != self.sequence.count(None):
                return False

            answer_idx = 0
            temp_sequence = self.sequence.copy()
            for i in range(len(temp_sequence)):
                if temp_sequence[i] is None:
                    temp_sequence[i] = user_answer[answer_idx]
                    answer_idx += 1

            return temp_sequence == self.solution

        elif self.type == MiniPuzzleType.PROBABILITY or self.type == MiniPuzzleType.QUANTUM_STATE:
            # Simple string comparison for probability and quantum state
            return user_answer.strip().lower() == self.solution.lower()

        return False

    def get_solution_format(self):
        if self.type == MiniPuzzleType.SEQUENCE or self.type == MiniPuzzleType.PATTERN:
            missing_count = self.sequence.count(None)
            return f"Enter {missing_count} values separated by spaces"
        elif self.type == MiniPuzzleType.PROBABILITY:
            return "Enter the probability as a fraction (e.g., 1/6)"
        elif self.type == MiniPuzzleType.QUANTUM_STATE:
            return "Enter the quantum state (e.g., |0⟩, |1⟩, |+⟩, or |-⟩)"

    def parse_user_input(self, user_input):
        if self.type == MiniPuzzleType.SEQUENCE:
            try:
                # Parse input as a list of integers
                return [int(x) for x in user_input.split()]
            except ValueError:
                return None
        elif self.type == MiniPuzzleType.PATTERN:
            # Return input as a list of strings
            return user_input.split()
        else:
            # Return as is for other puzzle types
            return user_input


class KuantumKitchen:
    def __init__(self):
        self.day = 1
        self.resources = {
            ResourceType.QUANTUM_ENERGY: 10,
            ResourceType.PROBABILITY_STABILIZER: 5,
            ResourceType.TIMELINE_TOKEN: 2
        }
        self.active_orders = []
        self.completed_orders = []
        self.failed_orders = []
        self.score = 0
        self.customer_satisfaction = 50  # Starting satisfaction level (%)
        self.reality_stability = 100  # Starting reality stability
        self.timelines = defaultdict(list)  # Tracks orders in each timeline
        self.current_phase = "Planning"
        self.max_active_orders = 3
        self.available_orders = []
        self.special_events = []
        self.kitchen_units = {
            "Quantum Stove": 1,
            "Probability Oven": 1,
            "Timeline Grill": 1
        }
        self.tutorial_shown = False

    def generate_orders(self):
        # Generate new available orders based on day and current game state
        num_orders = 3 + min(self.day // 2, 5)
        self.available_orders = []
        for _ in range(num_orders):
            self.available_orders.append(Order(self.day))

    def accept_order(self, order_idx):
        if order_idx < 0 or order_idx >= len(self.available_orders):
            return False, "Invalid order index"

        order = self.available_orders[order_idx]

        # Check if we have room for more orders
        if len(self.active_orders) >= self.max_active_orders:
            return False, f"You can only handle {self.max_active_orders} active orders at once"

        # Remove from available and add to active
        self.active_orders.append(order)
        self.timelines[order.timeline].append(order)
        self.available_orders.pop(order_idx)
        return True, f"Accepted order #{order.id}"

    def reject_order(self, order_idx):
        if order_idx < 0 or order_idx >= len(self.available_orders):
            return False, "Invalid order index"

        self.available_orders.pop(order_idx)
        # Small penalty for rejecting orders
        self.customer_satisfaction = max(0, self.customer_satisfaction - 2)
        return True, "Order rejected"

    def prepare_order(self, order_idx):
        if order_idx < 0 or order_idx >= len(self.active_orders):
            return False, "Invalid order index"

        order = self.active_orders[order_idx]

        # Check if order is in a valid state
        if order.state != OrderState.SUPERPOSITION:
            return False, f"Cannot prepare order in {order.state.value} state"

        # Check if we have enough resources
        for resource, amount in order.resource_requirements.items():
            if self.resources[resource] < amount:
                return False, f"Not enough {resource.value}"

        # Start mini-puzzle for this order
        puzzle = MiniPuzzle(order)
        puzzle_completed = self.solve_puzzle(puzzle)

        # Player gets a probability bonus based on puzzle success
        probability_bonus = 0.2 if puzzle_completed else 0

        # Consume resources
        for resource, amount in order.resource_requirements.items():
            self.resources[resource] -= amount

        # Collapse the order's quantum state
        order.collapse_state(probability_bonus)

        # Update satisfaction based on outcome
        satisfaction_delta = (order.actual_outcome["satisfaction"] - 50) / 10
        self.customer_satisfaction = min(100, max(0, self.customer_satisfaction + satisfaction_delta))

        # Reward
        final_reward = int(order.reward * order.actual_outcome["reward_multiplier"])
        self.score += final_reward

        # Handle reality stability effects
        if order.actual_outcome["satisfaction"] < 50:
            stability_loss = (50 - order.actual_outcome["satisfaction"]) / 10
            self.reality_stability = max(0, self.reality_stability - stability_loss)
            message = f"Prepared order #{order.id} ({order.actual_outcome['description']}). Reality distortion detected!"
        else:
            message = f"Prepared order #{order.id} ({order.actual_outcome['description']}). Earned {final_reward} points."

        # Refund some resources based on outcome quality
        if order.actual_outcome["satisfaction"] >= 80:
            refund_resource = random.choice(list(ResourceType))
            refund_amount = 1 + (1 if order.actual_outcome["satisfaction"] >= 90 else 0)
            self.resources[refund_resource] += refund_amount
            message += f" Gained {refund_amount} {refund_resource.value}!"

        return True, message

    def solve_puzzle(self, puzzle):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== QUANTUM KITCHEN MINI-PUZZLE =====")
        print(f"Order #{puzzle.order.id}: {puzzle.order.dish.value}")
        print(f"Puzzle Type: {puzzle.type.value}")
        print("\n" + puzzle.get_puzzle_description())
        print("\n" + puzzle.get_solution_format())

        # Give player three attempts
        for attempt in range(3):
            try:
                user_input = input(f"\nAttempt {attempt + 1}/3: ")
                answer = puzzle.parse_user_input(user_input)

                if answer is None:
                    print("Invalid input format. Please try again.")
                    continue

                if puzzle.check_solution(answer):
                    print("\nCorrect! Quantum state stabilized!")
                    time.sleep(1.5)
                    return True
                else:
                    print("Incorrect. Try again.")
            except Exception as e:
                print(f"Error: {e}")
                print("Invalid input. Please try again.")

        print("\nPuzzle failed. The order's quantum state is becoming unstable!")
        print(f"The correct solution was: {puzzle.solution}")
        time.sleep(2)
        return False

    def deliver_order(self, order_idx):
        if order_idx < 0 or order_idx >= len(self.active_orders):
            return False, "Invalid order index"

        order = self.active_orders[order_idx]

        # Check if order is ready for delivery
        if order.state != OrderState.COLLAPSED:
            return False, f"Cannot deliver order in {order.state.value} state"

        # Transfer from active to completed
        self.active_orders.pop(order_idx)
        self.completed_orders.append(order)

        # Remove from timeline
        if order in self.timelines[order.timeline]:
            self.timelines[order.timeline].remove(order)

        # Update order state
        order.state = OrderState.DELIVERED

        # Give resources based on satisfaction
        resource_reward = order.actual_outcome["satisfaction"] // 20  # 0-5 resources
        if resource_reward > 0:
            for _ in range(resource_reward):
                resource = random.choice(list(ResourceType))
                self.resources[resource] += 1

        return True, f"Delivered order #{order.id}. Customer satisfaction: {order.actual_outcome['satisfaction']}%"

    def update_time(self):
        # Update time for all active orders
        expired_orders = []

        for order in self.active_orders:
            if order.state == OrderState.SUPERPOSITION:
                if order.update_time():
                    expired_orders.append(order)

        # Handle expired orders
        for order in expired_orders:
            self.active_orders.remove(order)
            self.failed_orders.append(order)

            # Update customer satisfaction and reality stability
            self.customer_satisfaction = max(0, self.customer_satisfaction - 5)
            self.reality_stability = max(0, self.reality_stability - 5)

            # Display message
            print(f"Order #{order.id} has expired! Reality destabilized!")

        return len(expired_orders) > 0

    def advance_day(self):
        # Generate random events
        if random.random() < 0.3:
            self.trigger_special_event()

        # Restore some resources
        daily_resources = {
            ResourceType.QUANTUM_ENERGY: 5 + self.day // 2,
            ResourceType.PROBABILITY_STABILIZER: 2 + self.day // 3,
            ResourceType.TIMELINE_TOKEN: 1 + self.day // 4
        }

        for resource, amount in daily_resources.items():
            self.resources[resource] += amount

        # Restore some reality stability
        stability_gain = 5 + (self.customer_satisfaction // 20)
        self.reality_stability = min(100, self.reality_stability + stability_gain)

        # Increment day
        self.day += 1

        # Update max orders based on progress
        self.max_active_orders = 3 + min(self.day // 3, 4)

        return f"Day {self.day} begins! Customer satisfaction: {self.customer_satisfaction}%. Reality stability: {self.reality_stability}%"

    def trigger_special_event(self):
        event = random.choice(list(TimelineEvent))
        self.special_events.append(event)

        message = f"SPECIAL EVENT: {event.value}!"

        if event == TimelineEvent.RESOURCE_BOOST:
            resource = random.choice(list(ResourceType))
            amount = random.randint(2, 5)
            self.resources[resource] += amount
            message += f" Gained {amount} {resource.value}!"

        elif event == TimelineEvent.TIMELINE_SHIFT:
            # Shuffle timelines
            all_orders = []
            for timeline, orders in self.timelines.items():
                all_orders.extend(orders)

            # Reset timelines
            self.timelines = defaultdict(list)

            # Reassign orders to random timelines
            for order in all_orders:
                order.timeline = random.randint(1, min(2 + self.day // 3, 5))
                self.timelines[order.timeline].append(order)

            message += " All orders have shifted to different timelines!"

        elif event == TimelineEvent.QUANTUM_FLUCTUATION:
            # Randomly change the state of one order
            if self.active_orders:
                order = random.choice(self.active_orders)
                if order.state == OrderState.SUPERPOSITION:
                    order.time_remaining = min(order.time_limit, order.time_remaining + 2)
                    message += f" Order #{order.id} gained 2 time units!"

        elif event == TimelineEvent.REALITY_DISTORTION:
            # Minor negative effect
            stability_loss = random.randint(5, 15)
            self.reality_stability = max(0, self.reality_stability - stability_loss)
            message += f" Reality stability reduced by {stability_loss}%!"

        return message

    def get_status(self):
        status = [
            f"===== KUANTUM KITCHEN - DAY {self.day} =====",
            f"Phase: {self.current_phase}",
            f"Score: {self.score}",
            f"Customer Satisfaction: {self.customer_satisfaction}%",
            f"Reality Stability: {self.reality_stability}%",
            "",
            "Resources:",
        ]

        for resource, amount in self.resources.items():
            status.append(f"  {resource.value}: {amount}")

        status.append("")
        status.append(
            f"Kitchen Units: {', '.join([f'{unit} (x{count})' for unit, count in self.kitchen_units.items()])}")
        status.append("")

        if self.special_events:
            status.append("Active Events:")
            for event in self.special_events:
                status.append(f"  {event.value}")
            status.append("")

        return "\n".join(status)

    def show_tutorial(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== WELCOME TO KUANTUM KITCHEN =====")
        print("\nYou are the manager of a quantum kitchen where orders exist in superposition until observed!")
        print("\nGAME PHASES:")
        print("1. PLANNING: Accept orders and allocate resources")
        print("2. EXECUTION: Prepare orders by solving mini-puzzles and using resources")
        print("3. DELIVERY: Deliver completed orders to customers")

        print("\nKEY CONCEPTS:")
        print("- Orders exist in SUPERPOSITION until prepared")
        print("- When prepared, orders COLLAPSE into a specific dish quality")
        print("- Failed orders cause REALITY DISTORTIONS that permanently affect the game")
        print("- Maintain CUSTOMER SATISFACTION and REALITY STABILITY to succeed")

        print("\nRESOURCES:")
        print("- Quantum Energy: Powers your kitchen operations")
        print("- Probability Stabilizers: Increase chances of successful dishes")
        print("- Timeline Tokens: Help manage deliveries across multiple timelines")

        input("\nPress ENTER to start your first day at Kuantum Kitchen...")
        self.tutorial_shown = True

    def check_game_over(self):
        # Game over if reality stability hits 0
        if self.reality_stability <= 0:
            return True, "GAME OVER: Reality has completely collapsed!"

        # Game over if customer satisfaction hits 0
        if self.customer_satisfaction <= 0:
            return True, "GAME OVER: Your restaurant has lost all its customers!"

        return False, ""

    def run_planning_phase(self):
        self.current_phase = "Planning"
        self.generate_orders()

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self.get_status())

            print("\n===== AVAILABLE ORDERS =====")
            if not self.available_orders:
                print("No more orders available.")
            else:
                for i, order in enumerate(self.available_orders):
                    print(f"[{i + 1}] {order}")

            print("\n===== ACTIVE ORDERS =====")
            if not self.active_orders:
                print("No active orders.")
            else:
                for i, order in enumerate(self.active_orders):
                    print(f"[{i + 1}] {order}")

            print("\n===== PLANNING PHASE COMMANDS =====")
            print("[a#] Accept order # (e.g., a1)")
            print("[r#] Reject order # (e.g., r1)")
            print("[v#] View order details # (e.g., v1)")
            print("[n] Proceed to Execution Phase")
            print("[q] Quit game")

            command = input("\nEnter command: ").strip().lower()

            if command == 'q':
                if input("Are you sure you want to quit? (y/n): ").lower() == 'y':
                    return False
            elif command == 'n':
                if not self.active_orders:
                    print("You must accept at least one order to proceed.")
                    input("Press ENTER to continue...")
                else:
                    return True
            elif command.startswith('a'):
                try:
                    order_idx = int(command[1:]) - 1
                    success, message = self.accept_order(order_idx)
                    print(message)
                    input("Press ENTER to continue...")
                except (ValueError, IndexError):
                    print("Invalid command format. Use a# to accept an order.")
                    input("Press ENTER to continue...")
            elif command.startswith('r'):
                try:
                    order_idx = int(command[1:]) - 1
                    success, message = self.reject_order(order_idx)
                    print(message)
                    input("Press ENTER to continue...")
                except (ValueError, IndexError):
                    print("Invalid command format. Use r# to reject an order.")
                    input("Press ENTER to continue...")
            elif command.startswith('v'):
                try:
                    if command[1] == 'a':  # View active order
                        order_idx = int(command[2:]) - 1
                        if 0 <= order_idx < len(self.active_orders):
                            print("\n" + self.active_orders[order_idx].get_details())
                        else:
                            print("Invalid order index.")
                    else:  # View available order
                        order_idx = int(command[1:]) - 1
                        if 0 <= order_idx < len(self.available_orders):
                            print("\n" + self.available_orders[order_idx].get_details())
                        else:
                            print("Invalid order index.")
                    input("Press ENTER to continue...")
                except (ValueError, IndexError):
                    print("Invalid command format. Use v# to view an order.")
                    input("Press ENTER to continue...")
            else:
                print("Invalid command.")
                input("Press ENTER to continue...")

            def run_execution_phase(self):
                self.current_phase = "Execution"

                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(self.get_status())

                    print("\n===== ACTIVE ORDERS =====")
                    if not self.active_orders:
                        print("No active orders. All orders have been prepared!")
                        input("Press ENTER to continue to Delivery Phase...")
                        return True
                    else:
                        for i, order in enumerate(self.active_orders):
                            print(f"[{i + 1}] {order}")

                    print("\n===== TIMELINES =====")
                    for timeline, orders in sorted(self.timelines.items()):
                        if orders:
                            order_ids = [str(order.id) for order in orders]
                            print(f"Timeline {timeline}: Orders #{', #'.join(order_ids)}")

                    print("\n===== EXECUTION PHASE COMMANDS =====")
                    print("[p#] Prepare order # (e.g., p1)")
                    print("[v#] View order details # (e.g., v1)")
                    print("[t] Update time (advances time by 1 unit)")
                    print("[n] Proceed to Delivery Phase")
                    print("[q] Quit game")

                    command = input("\nEnter command: ").strip().lower()

                    if command == 'q':
                        if input("Are you sure you want to quit? (y/n): ").lower() == 'y':
                            return False
                    elif command == 'n':
                        ready_to_proceed = True
                        for order in self.active_orders:
                            if order.state == OrderState.SUPERPOSITION:
                                ready_to_proceed = False
                                break

                        if ready_to_proceed:
                            return True
                        else:
                            print("You must prepare all orders before proceeding.")
                            input("Press ENTER to continue...")
                    elif command == 't':
                        if self.update_time():
                            input("Press ENTER to continue...")
                    elif command.startswith('p'):
                        try:
                            order_idx = int(command[1:]) - 1
                            success, message = self.prepare_order(order_idx)
                            print(message)
                            input("Press ENTER to continue...")
                        except (ValueError, IndexError):
                            print("Invalid command format. Use p# to prepare an order.")
                            input("Press ENTER to continue...")
                    elif command.startswith('v'):
                        try:
                            order_idx = int(command[1:]) - 1
                            if 0 <= order_idx < len(self.active_orders):
                                print("\n" + self.active_orders[order_idx].get_details())
                            else:
                                print("Invalid order index.")
                            input("Press ENTER to continue...")
                        except (ValueError, IndexError):
                            print("Invalid command format. Use v# to view an order.")
                            input("Press ENTER to continue...")
                    else:
                        print("Invalid command.")
                        input("Press ENTER to continue...")

            def run_delivery_phase(self):
                self.current_phase = "Delivery"

                while True:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print(self.get_status())

                    print("\n===== ACTIVE ORDERS =====")
                    if not self.active_orders:
                        print("No active orders. All orders have been delivered!")
                        input("Press ENTER to continue to the next day...")
                        return True
                    else:
                        for i, order in enumerate(self.active_orders):
                            print(f"[{i + 1}] {order}")

                    print("\n===== TIMELINES =====")
                    for timeline, orders in sorted(self.timelines.items()):
                        if orders:
                            order_ids = [str(order.id) for order in orders]
                            print(f"Timeline {timeline}: Orders #{', #'.join(order_ids)}")

                    print("\n===== DELIVERY PHASE COMMANDS =====")
                    print("[d#] Deliver order # (e.g., d1)")
                    print("[v#] View order details # (e.g., v1)")
                    print("[n] End day and proceed to next day")
                    print("[q] Quit game")

                    command = input("\nEnter command: ").strip().lower()

                    if command == 'q':
                        if input("Are you sure you want to quit? (y/n): ").lower() == 'y':
                            return False
                    elif command == 'n':
                        if self.active_orders:
                            if input(
                                    "You still have active orders. Are you sure you want to end the day? (y/n): ").lower() == 'y':
                                # Failed delivery penalty
                                for order in self.active_orders:
                                    self.customer_satisfaction = max(0, self.customer_satisfaction - 3)

                                self.active_orders = []
                                self.timelines = defaultdict(list)
                                return True
                        else:
                            return True
                    elif command.startswith('d'):
                        try:
                            order_idx = int(command[1:]) - 1
                            success, message = self.deliver_order(order_idx)
                            print(message)
                            input("Press ENTER to continue...")
                        except (ValueError, IndexError):
                            print("Invalid command format. Use d# to deliver an order.")
                            input("Press ENTER to continue...")
                    elif command.startswith('v'):
                        try:
                            order_idx = int(command[1:]) - 1
                            if 0 <= order_idx < len(self.active_orders):
                                print("\n" + self.active_orders[order_idx].get_details())
                            else:
                                print("Invalid order index.")
                            input("Press ENTER to continue...")
                        except (ValueError, IndexError):
                            print("Invalid command format. Use v# to view an order.")
                            input("Press ENTER to continue...")
                    else:
                        print("Invalid command.")
                        input("Press ENTER to continue...")

            def show_game_summary(self):
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n===== KUANTUM KITCHEN SUMMARY =====")
                print(f"Days Survived: {self.day}")
                print(f"Final Score: {self.score}")
                print(f"Customer Satisfaction: {self.customer_satisfaction}%")
                print(f"Reality Stability: {self.reality_stability}%")
                print(f"Orders Completed: {len(self.completed_orders)}")
                print(f"Orders Failed: {len(self.failed_orders)}")

                print("\nTop 5 Best Orders:")
                best_orders = sorted(self.completed_orders,
                                     key=lambda o: o.actual_outcome["satisfaction"] if o.actual_outcome else 0,
                                     reverse=True)[:5]
                for i, order in enumerate(best_orders):
                    if order.actual_outcome:
                        print(
                            f"{i + 1}. Order #{order.id}: {order.dish.value} - {order.actual_outcome['description']} ({order.actual_outcome['satisfaction']}%)")

                input("\nPress ENTER to exit...")

            def run_game(self):
                if not self.tutorial_shown:
                    self.show_tutorial()

                game_running = True

                while game_running:
                    # Start day with planning phase
                    message = self.advance_day()
                    print(message)

                    # Check for game over
                    game_over, reason = self.check_game_over()
                    if game_over:
                        print(reason)
                        input("Press ENTER to continue...")
                        break

                    # Planning Phase
                    if not self.run_planning_phase():
                        break

                    # Execution Phase
                    if not self.run_execution_phase():
                        break

                    # Delivery Phase
                    if not self.run_delivery_phase():
                        break

                self.show_game_summary()


def main():
    try:
        # Initialize and run the game
        game = KuantumKitchen()
        game.run_game()
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("\nThank you for playing Kuantum Kitchen!")


if __name__ == "__main__":
    main()
