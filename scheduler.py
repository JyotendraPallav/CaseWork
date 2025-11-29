import random
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Task:
    id: int
    tokens: int
    case_code: str = "" # Added case_code

@dataclass
class Leader:
    name: str
    daily_limit: int
    target_ratio_weight: int
    
    # Computed during allocation
    target_tokens: int = 0
    current_tokens: int = 0
    assigned_tasks: List[Task] = field(default_factory=list)
    
    # Computed during scheduling
    schedule: List[List[Task]] = field(default_factory=list) # List of days, each day is a list of tasks

    def remaining_need(self) -> int:
        return self.target_tokens - self.current_tokens

def solve_scheduling(tasks: List[Task], leaders: List[Leader]) -> List[Dict[str, Any]]:
    """
    Main solver function.
    Returns a list of dictionaries representing the daily schedule.
    """
    
    # --- Phase 1: Allocation (Target Ratio) ---
    total_tokens = sum(t.tokens for t in tasks)
    total_ratio = sum(l.target_ratio_weight for l in leaders)
    
    if total_ratio == 0:
        raise ValueError("Total ratio weight cannot be zero.")

    # Calculate target tokens for each leader
    for leader in leaders:
        leader.target_tokens = int(total_tokens * (leader.target_ratio_weight / total_ratio))
    
    # Adjust for rounding errors
    allocated_target = sum(l.target_tokens for l in leaders)
    diff = total_tokens - allocated_target
    if diff != 0:
        leaders[0].target_tokens += diff

    # Sort tasks by size (descending)
    sorted_tasks = sorted(tasks, key=lambda t: t.tokens, reverse=True)
    
    # Greedy allocation
    for task in sorted_tasks:
        best_leader = max(leaders, key=lambda l: l.target_tokens - l.current_tokens)
        best_leader.assigned_tasks.append(task)
        best_leader.current_tokens += task.tokens

    # --- Phase 2: Scheduling (Daily Capacity) ---
    # Bin Packing (First Fit Decreasing)
    
    schedule_data = []

    for leader in leaders:
        leader_tasks = sorted(leader.assigned_tasks, key=lambda t: t.tokens, reverse=True)
        
        days: List[List[Task]] = []
        day_sums: List[int] = []
        
        for task in leader_tasks:
            placed = False
            for i in range(len(days)):
                if day_sums[i] + task.tokens <= leader.daily_limit:
                    days[i].append(task)
                    day_sums[i] += task.tokens
                    placed = True
                    break
            
            if not placed:
                if task.tokens > leader.daily_limit:
                    # If a single task exceeds the limit, we must still assign it but it will overflow
                    # Ideally we warn, but for now we just put it in a new day
                    pass 
                days.append([task])
                day_sums.append(task.tokens)
        
        leader.schedule = days
        
        # Flatten for output
        for day_idx, day_tasks in enumerate(days):
            for task in day_tasks:
                schedule_data.append({
                    "Day": day_idx + 1,
                    "Manager": leader.name,
                    "Case Code": task.case_code,
                    "Billing Amount": task.tokens,
                    "Daily Load": day_sums[day_idx], # Current load for this day
                    "Max Load": leader.daily_limit
                })

    return schedule_data

def main():
    # Sample run
    tasks = [Task(id=i, tokens=random.randint(10, 100), case_code=f"CASE-{i}") for i in range(50)]
    leaders = [
        Leader(name="Leader X", daily_limit=150, target_ratio_weight=2),
        Leader(name="Leader Y", daily_limit=200, target_ratio_weight=3),
        Leader(name="Leader Z", daily_limit=250, target_ratio_weight=5),
    ]
    
    result = solve_scheduling(tasks, leaders)
    print(f"Scheduled {len(result)} items.")
    print(result[:5])

if __name__ == "__main__":
    main()
