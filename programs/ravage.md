# GVS Ravage

Source-of-truth program definition. Weeks 1–9 are the steady-state block: identical
exercise selection, set/rep targets, RIR, rest, and superset structure — weight
progression happens automatically via each exercise's `progress:` rule as sessions
are actually completed, not through hand-edited per-week numbers. Week 10 is the
deload: volume trimmed to one set per exercise and `progress: none` to freeze
weight, per Schofield's auto-regulated approach to unloading.

# Week 1
## Day 1 - Legs A
prog / used: none / 1x1 / 0lb / progress: custom(increment: 5lb) {~
  if (completedReps >= reps) {
    weights += state.increment
  }
~}
Hack Squat, Smith Machine / 1x10-10, 1x13-15, 1x9-15 / @8+ 180s / progress: custom() { ...prog }
Stiff Leg Deadlift, Dumbbell / 1x11-15, 1x9-15 / @9+ 120s / progress: custom() { ...prog }
dpz: Walking Lunge / 2x12-30 / 15lb @10+ 120s / progress: custom() { ...prog }
dpz: Lying Leg Curl / 1x10-12, 1x12-12 / @10+ 90s / progress: custom() { ...prog }

## Day 2 - Torso A
Smith Machine Close Grip Larsen Press / 1x7-8 120lb, 2x5-8 130lb / @9+ 120s / superset: A / progress: custom() { ...prog }
Narrow: Narrow Pulldown / 1x10-15+ 97.5lb, 1x5-15+ 100lb, 1x3-15+ 100lb / @9+ 90s / superset: A / progress: custom() { ...prog }
Smith Reverse Grip Bench / 1x9-12, 1x7-12 / 90lb @9+ 120s / superset: B / progress: custom() { ...prog }
Wide: Machine Pulldown / 1x13-15 135lb, 1x12-15 127.5lb / @9+ 90s / superset: B / progress: custom() { ...prog }
Cable Crossover / 1x11-15, 1x9-15 / 22.5lb @10+ 60s / superset: C / progress: custom(increment: 2.5lb) { ...prog }
Bent Over One Arm Row / 1x15-15 50lb, 1x9-15 / @10+ 120s / superset: C / progress: custom() { ...prog }
Pullover, Cable / 1x18-20 22.5lb, 1x14-20 27.5lb / @10+ 60s / progress: custom(increment: 2.5lb) { ...prog }

## Day 3 - Bro Day A
Hammer Curl / 1x10-20 25lb, 1x12-20 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
Triceps Pushdown / 1x12-15 60lb, 1x8-15 / @10+ 90s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
Incline Curl / 1x6-10 22lb, 1x6-10 / @10+ 60s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
Triceps Extension, Cable / 1x12-15, 1x14-15 / 47.5lb @10+ 90s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
dfd: Lateral Raise / 1x8-15, 1x10-15 / 26lb @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Upright Row / 1x13-20 25lb, 1x12-20 / @10+ 90s / progress: custom(increment: 2.5lb) { ...prog }

## Day 4 - Legs B
Squat, Smith Machine / 1x6-8, 1x5-8 / 130lb @9+ 210s / progress: custom() { ...prog }
Romanian Deadlift / 1x8-12, 1x5-12 / 70lb @9+ 120s / progress: custom() { ...prog }
Lying Leg Curl / 1x8-15 37.5lb, 1x8-15 / @10+ 90s / progress: custom() { ...prog }
Leg Extension / 1x13-20, 1x10-20 / @10+ 90s / progress: custom() { ...prog }
Standing Calf Raise, Barbell / 1x15-20 / 160lb @10+ 90s / progress: custom() { ...prog }

## Day 5 - Torso B
B: Bench Press, Dumbbell / 1x7-12, 1x9-12 / 70lb @9+ 120s / superset: A / progress: custom() { ...prog }
B: Machine Pulldown / 1x10-15, 1x8-15 / 130lb @10+ 90s / superset: A / progress: custom() { ...prog }
B: Chest Press, Leverage Machine / 2x9-12 / @9+ 120s / superset: B / progress: custom() { ...prog }
B: Helms Row / 1x12-20, 1x14-20 / 45lb @10+ 90s / superset: B / progress: custom() { ...prog }
B: Shoulder Press / 1x9-12, 1x6-12 / @9+ 120s / superset: C / progress: custom() { ...prog }
Seated Row / 1x17-20 77.5lb, 1x17-20 80lb / @10+ 90s / superset: C / progress: custom(increment: 2.5lb) { ...prog }

## Day 6 - Bro Day B
BroB: Hammer Curl / 1x12-20, 1x13-20 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
BroB: Triceps Extension, Cable / 1x15-15, 1x13-15 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
BroB: Bicep Curl / 1x10-12, 1x9-12 / @10+ 45s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
BroB: Triceps Pushdown / 1x8-15, 1x7-15 / @10+ 90s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
BroB: Lateral Raise / 1x13-20, 1x10-20 / @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Lu Lateral Raise / 2x10-15 / 10lb @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Cable Rear Delt One-Arm Row / 2x15-20 / 12.5lb @10+ 60s / progress: custom(increment: 2.5lb) { ...prog }
BroB: Neck Flexion / 1x4-20 / 3.5lb @10+ 30s / progress: custom(increment: 1lb) { ...prog }
BroB: Wrist Curl, Dumbbell / 1x14-20 / 24lb @10+ 30s / progress: custom(increment: 1lb) { ...prog }


# Week 2
## Day 1 - Legs A
Hack Squat, Smith Machine / 1x10-10, 1x13-15, 1x9-15 / @8+ 180s / progress: custom() { ...prog }
Stiff Leg Deadlift, Dumbbell / 1x11-15, 1x9-15 / @9+ 120s / progress: custom() { ...prog }
dpz: Walking Lunge / 2x12-30 / 15lb @10+ 120s / progress: custom() { ...prog }
dpz: Lying Leg Curl / 1x10-12, 1x12-12 / @10+ 90s / progress: custom() { ...prog }

## Day 2 - Torso A
Smith Machine Close Grip Larsen Press / 1x7-8 120lb, 2x5-8 130lb / @9+ 120s / superset: A / progress: custom() { ...prog }
Narrow: Narrow Pulldown / 1x10-15+ 97.5lb, 1x5-15+ 100lb, 1x3-15+ 100lb / @9+ 90s / superset: A / progress: custom() { ...prog }
Smith Reverse Grip Bench / 1x9-12, 1x7-12 / 90lb @9+ 120s / superset: B / progress: custom() { ...prog }
Wide: Machine Pulldown / 1x13-15 135lb, 1x12-15 127.5lb / @9+ 90s / superset: B / progress: custom() { ...prog }
Cable Crossover / 1x11-15, 1x9-15 / 22.5lb @10+ 60s / superset: C / progress: custom(increment: 2.5lb) { ...prog }
Bent Over One Arm Row / 1x15-15 50lb, 1x9-15 / @10+ 120s / superset: C / progress: custom() { ...prog }
Pullover, Cable / 1x18-20 22.5lb, 1x14-20 27.5lb / @10+ 60s / progress: custom(increment: 2.5lb) { ...prog }

## Day 3 - Bro Day A
Hammer Curl / 1x10-20 25lb, 1x12-20 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
Triceps Pushdown / 1x12-15 60lb, 1x8-15 / @10+ 90s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
Incline Curl / 1x6-10 22lb, 1x6-10 / @10+ 60s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
Triceps Extension, Cable / 1x12-15, 1x14-15 / 47.5lb @10+ 90s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
dfd: Lateral Raise / 1x8-15, 1x10-15 / 26lb @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Upright Row / 1x13-20 25lb, 1x12-20 / @10+ 90s / progress: custom(increment: 2.5lb) { ...prog }

## Day 4 - Legs B
Squat, Smith Machine / 1x6-8, 1x5-8 / 130lb @9+ 210s / progress: custom() { ...prog }
Romanian Deadlift / 1x8-12, 1x5-12 / 70lb @9+ 120s / progress: custom() { ...prog }
Lying Leg Curl / 1x8-15 37.5lb, 1x8-15 / @10+ 90s / progress: custom() { ...prog }
Leg Extension / 1x13-20, 1x10-20 / @10+ 90s / progress: custom() { ...prog }
Standing Calf Raise, Barbell / 1x15-20 / 160lb @10+ 90s / progress: custom() { ...prog }

## Day 5 - Torso B
B: Bench Press, Dumbbell / 1x7-12, 1x9-12 / 70lb @9+ 120s / superset: A / progress: custom() { ...prog }
B: Machine Pulldown / 1x10-15, 1x8-15 / 130lb @10+ 90s / superset: A / progress: custom() { ...prog }
B: Chest Press, Leverage Machine / 2x9-12 / @9+ 120s / superset: B / progress: custom() { ...prog }
B: Helms Row / 1x12-20, 1x14-20 / 45lb @10+ 90s / superset: B / progress: custom() { ...prog }
B: Shoulder Press / 1x9-12, 1x6-12 / @9+ 120s / superset: C / progress: custom() { ...prog }
Seated Row / 1x17-20 77.5lb, 1x17-20 80lb / @10+ 90s / superset: C / progress: custom(increment: 2.5lb) { ...prog }

## Day 6 - Bro Day B
BroB: Hammer Curl / 1x12-20, 1x13-20 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
BroB: Triceps Extension, Cable / 1x15-15, 1x13-15 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
BroB: Bicep Curl / 1x10-12, 1x9-12 / @10+ 45s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
BroB: Triceps Pushdown / 1x8-15, 1x7-15 / @10+ 90s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
BroB: Lateral Raise / 1x13-20, 1x10-20 / @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Lu Lateral Raise / 2x10-15 / 10lb @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Cable Rear Delt One-Arm Row / 2x15-20 / 12.5lb @10+ 60s / progress: custom(increment: 2.5lb) { ...prog }
BroB: Neck Flexion / 1x4-20 / 3.5lb @10+ 30s / progress: custom(increment: 1lb) { ...prog }
BroB: Wrist Curl, Dumbbell / 1x14-20 / 24lb @10+ 30s / progress: custom(increment: 1lb) { ...prog }


# Week 3
## Day 1 - Legs A
Hack Squat, Smith Machine / 1x10-10, 1x13-15, 1x9-15 / @8+ 180s / progress: custom() { ...prog }
Stiff Leg Deadlift, Dumbbell / 1x11-15, 1x9-15 / @9+ 120s / progress: custom() { ...prog }
dpz: Walking Lunge / 2x12-30 / 15lb @10+ 120s / progress: custom() { ...prog }
dpz: Lying Leg Curl / 1x10-12, 1x12-12 / @10+ 90s / progress: custom() { ...prog }

## Day 2 - Torso A
Smith Machine Close Grip Larsen Press / 1x7-8 120lb, 2x5-8 130lb / @9+ 120s / superset: A / progress: custom() { ...prog }
Narrow: Narrow Pulldown / 1x10-15+ 97.5lb, 1x5-15+ 100lb, 1x3-15+ 100lb / @9+ 90s / superset: A / progress: custom() { ...prog }
Smith Reverse Grip Bench / 1x9-12, 1x7-12 / 90lb @9+ 120s / superset: B / progress: custom() { ...prog }
Wide: Machine Pulldown / 1x13-15 135lb, 1x12-15 127.5lb / @9+ 90s / superset: B / progress: custom() { ...prog }
Cable Crossover / 1x11-15, 1x9-15 / 22.5lb @10+ 60s / superset: C / progress: custom(increment: 2.5lb) { ...prog }
Bent Over One Arm Row / 1x15-15 50lb, 1x9-15 / @10+ 120s / superset: C / progress: custom() { ...prog }
Pullover, Cable / 1x18-20 22.5lb, 1x14-20 27.5lb / @10+ 60s / progress: custom(increment: 2.5lb) { ...prog }

## Day 3 - Bro Day A
Hammer Curl / 1x10-20 25lb, 1x12-20 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
Triceps Pushdown / 1x12-15 60lb, 1x8-15 / @10+ 90s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
Incline Curl / 1x6-10 22lb, 1x6-10 / @10+ 60s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
Triceps Extension, Cable / 1x12-15, 1x14-15 / 47.5lb @10+ 90s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
dfd: Lateral Raise / 1x8-15, 1x10-15 / 26lb @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Upright Row / 1x13-20 25lb, 1x12-20 / @10+ 90s / progress: custom(increment: 2.5lb) { ...prog }

## Day 4 - Legs B
Squat, Smith Machine / 1x6-8, 1x5-8 / 130lb @9+ 210s / progress: custom() { ...prog }
Romanian Deadlift / 1x8-12, 1x5-12 / 70lb @9+ 120s / progress: custom() { ...prog }
Lying Leg Curl / 1x8-15 37.5lb, 1x8-15 / @10+ 90s / progress: custom() { ...prog }
Leg Extension / 1x13-20, 1x10-20 / @10+ 90s / progress: custom() { ...prog }
Standing Calf Raise, Barbell / 1x15-20 / 160lb @10+ 90s / progress: custom() { ...prog }

## Day 5 - Torso B
B: Bench Press, Dumbbell / 1x7-12, 1x9-12 / 70lb @9+ 120s / superset: A / progress: custom() { ...prog }
B: Machine Pulldown / 1x10-15, 1x8-15 / 130lb @10+ 90s / superset: A / progress: custom() { ...prog }
B: Chest Press, Leverage Machine / 2x9-12 / @9+ 120s / superset: B / progress: custom() { ...prog }
B: Helms Row / 1x12-20, 1x14-20 / 45lb @10+ 90s / superset: B / progress: custom() { ...prog }
B: Shoulder Press / 1x9-12, 1x6-12 / @9+ 120s / superset: C / progress: custom() { ...prog }
Seated Row / 1x17-20 77.5lb, 1x17-20 80lb / @10+ 90s / superset: C / progress: custom(increment: 2.5lb) { ...prog }

## Day 6 - Bro Day B
BroB: Hammer Curl / 1x12-20, 1x13-20 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
BroB: Triceps Extension, Cable / 1x15-15, 1x13-15 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
BroB: Bicep Curl / 1x10-12, 1x9-12 / @10+ 45s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
BroB: Triceps Pushdown / 1x8-15, 1x7-15 / @10+ 90s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
BroB: Lateral Raise / 1x13-20, 1x10-20 / @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Lu Lateral Raise / 2x10-15 / 10lb @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Cable Rear Delt One-Arm Row / 2x15-20 / 12.5lb @10+ 60s / progress: custom(increment: 2.5lb) { ...prog }
BroB: Neck Flexion / 1x4-20 / 3.5lb @10+ 30s / progress: custom(increment: 1lb) { ...prog }
BroB: Wrist Curl, Dumbbell / 1x14-20 / 24lb @10+ 30s / progress: custom(increment: 1lb) { ...prog }


# Week 4
## Day 1 - Legs A
Hack Squat, Smith Machine / 1x10-10, 1x13-15, 1x9-15 / @8+ 180s / progress: custom() { ...prog }
Stiff Leg Deadlift, Dumbbell / 1x11-15, 1x9-15 / @9+ 120s / progress: custom() { ...prog }
dpz: Walking Lunge / 2x12-30 / 15lb @10+ 120s / progress: custom() { ...prog }
dpz: Lying Leg Curl / 1x10-12, 1x12-12 / @10+ 90s / progress: custom() { ...prog }

## Day 2 - Torso A
Smith Machine Close Grip Larsen Press / 1x7-8 120lb, 2x5-8 130lb / @9+ 120s / superset: A / progress: custom() { ...prog }
Narrow: Narrow Pulldown / 1x10-15+ 97.5lb, 1x5-15+ 100lb, 1x3-15+ 100lb / @9+ 90s / superset: A / progress: custom() { ...prog }
Smith Reverse Grip Bench / 1x9-12, 1x7-12 / 90lb @9+ 120s / superset: B / progress: custom() { ...prog }
Wide: Machine Pulldown / 1x13-15 135lb, 1x12-15 127.5lb / @9+ 90s / superset: B / progress: custom() { ...prog }
Cable Crossover / 1x11-15, 1x9-15 / 22.5lb @10+ 60s / superset: C / progress: custom(increment: 2.5lb) { ...prog }
Bent Over One Arm Row / 1x15-15 50lb, 1x9-15 / @10+ 120s / superset: C / progress: custom() { ...prog }
Pullover, Cable / 1x18-20 22.5lb, 1x14-20 27.5lb / @10+ 60s / progress: custom(increment: 2.5lb) { ...prog }

## Day 3 - Bro Day A
Hammer Curl / 1x10-20 25lb, 1x12-20 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
Triceps Pushdown / 1x12-15 60lb, 1x8-15 / @10+ 90s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
Incline Curl / 1x6-10 22lb, 1x6-10 / @10+ 60s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
Triceps Extension, Cable / 1x12-15, 1x14-15 / 47.5lb @10+ 90s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
dfd: Lateral Raise / 1x8-15, 1x10-15 / 26lb @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Upright Row / 1x13-20 25lb, 1x12-20 / @10+ 90s / progress: custom(increment: 2.5lb) { ...prog }

## Day 4 - Legs B
Squat, Smith Machine / 1x6-8, 1x5-8 / 130lb @9+ 210s / progress: custom() { ...prog }
Romanian Deadlift / 1x8-12, 1x5-12 / 70lb @9+ 120s / progress: custom() { ...prog }
Lying Leg Curl / 1x8-15 37.5lb, 1x8-15 / @10+ 90s / progress: custom() { ...prog }
Leg Extension / 1x13-20, 1x10-20 / @10+ 90s / progress: custom() { ...prog }
Standing Calf Raise, Barbell / 1x15-20 / 160lb @10+ 90s / progress: custom() { ...prog }

## Day 5 - Torso B
B: Bench Press, Dumbbell / 1x7-12, 1x9-12 / 70lb @9+ 120s / superset: A / progress: custom() { ...prog }
B: Machine Pulldown / 1x10-15, 1x8-15 / 130lb @10+ 90s / superset: A / progress: custom() { ...prog }
B: Chest Press, Leverage Machine / 2x9-12 / @9+ 120s / superset: B / progress: custom() { ...prog }
B: Helms Row / 1x12-20, 1x14-20 / 45lb @10+ 90s / superset: B / progress: custom() { ...prog }
B: Shoulder Press / 1x9-12, 1x6-12 / @9+ 120s / superset: C / progress: custom() { ...prog }
Seated Row / 1x17-20 77.5lb, 1x17-20 80lb / @10+ 90s / superset: C / progress: custom(increment: 2.5lb) { ...prog }

## Day 6 - Bro Day B
BroB: Hammer Curl / 1x12-20, 1x13-20 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
BroB: Triceps Extension, Cable / 1x15-15, 1x13-15 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
BroB: Bicep Curl / 1x10-12, 1x9-12 / @10+ 45s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
BroB: Triceps Pushdown / 1x8-15, 1x7-15 / @10+ 90s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
BroB: Lateral Raise / 1x13-20, 1x10-20 / @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Lu Lateral Raise / 2x10-15 / 10lb @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Cable Rear Delt One-Arm Row / 2x15-20 / 12.5lb @10+ 60s / progress: custom(increment: 2.5lb) { ...prog }
BroB: Neck Flexion / 1x4-20 / 3.5lb @10+ 30s / progress: custom(increment: 1lb) { ...prog }
BroB: Wrist Curl, Dumbbell / 1x14-20 / 24lb @10+ 30s / progress: custom(increment: 1lb) { ...prog }


# Week 5
## Day 1 - Legs A
Hack Squat, Smith Machine / 1x10-10, 1x13-15, 1x9-15 / @8+ 180s / progress: custom() { ...prog }
Stiff Leg Deadlift, Dumbbell / 1x11-15, 1x9-15 / @9+ 120s / progress: custom() { ...prog }
dpz: Walking Lunge / 2x12-30 / 15lb @10+ 120s / progress: custom() { ...prog }
dpz: Lying Leg Curl / 1x10-12, 1x12-12 / @10+ 90s / progress: custom() { ...prog }

## Day 2 - Torso A
Smith Machine Close Grip Larsen Press / 1x7-8 120lb, 2x5-8 130lb / @9+ 120s / superset: A / progress: custom() { ...prog }
Narrow: Narrow Pulldown / 1x10-15+ 97.5lb, 1x5-15+ 100lb, 1x3-15+ 100lb / @9+ 90s / superset: A / progress: custom() { ...prog }
Smith Reverse Grip Bench / 1x9-12, 1x7-12 / 90lb @9+ 120s / superset: B / progress: custom() { ...prog }
Wide: Machine Pulldown / 1x13-15 135lb, 1x12-15 127.5lb / @9+ 90s / superset: B / progress: custom() { ...prog }
Cable Crossover / 1x11-15, 1x9-15 / 22.5lb @10+ 60s / superset: C / progress: custom(increment: 2.5lb) { ...prog }
Bent Over One Arm Row / 1x15-15 50lb, 1x9-15 / @10+ 120s / superset: C / progress: custom() { ...prog }
Pullover, Cable / 1x18-20 22.5lb, 1x14-20 27.5lb / @10+ 60s / progress: custom(increment: 2.5lb) { ...prog }

## Day 3 - Bro Day A
Hammer Curl / 1x10-20 25lb, 1x12-20 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
Triceps Pushdown / 1x12-15 60lb, 1x8-15 / @10+ 90s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
Incline Curl / 1x6-10 22lb, 1x6-10 / @10+ 60s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
Triceps Extension, Cable / 1x12-15, 1x14-15 / 47.5lb @10+ 90s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
dfd: Lateral Raise / 1x8-15, 1x10-15 / 26lb @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Upright Row / 1x13-20 25lb, 1x12-20 / @10+ 90s / progress: custom(increment: 2.5lb) { ...prog }

## Day 4 - Legs B
Squat, Smith Machine / 1x6-8, 1x5-8 / 130lb @9+ 210s / progress: custom() { ...prog }
Romanian Deadlift / 1x8-12, 1x5-12 / 70lb @9+ 120s / progress: custom() { ...prog }
Lying Leg Curl / 1x8-15 37.5lb, 1x8-15 / @10+ 90s / progress: custom() { ...prog }
Leg Extension / 1x13-20, 1x10-20 / @10+ 90s / progress: custom() { ...prog }
Standing Calf Raise, Barbell / 1x15-20 / 160lb @10+ 90s / progress: custom() { ...prog }

## Day 5 - Torso B
B: Bench Press, Dumbbell / 1x7-12, 1x9-12 / 70lb @9+ 120s / superset: A / progress: custom() { ...prog }
B: Machine Pulldown / 1x10-15, 1x8-15 / 130lb @10+ 90s / superset: A / progress: custom() { ...prog }
B: Chest Press, Leverage Machine / 2x9-12 / @9+ 120s / superset: B / progress: custom() { ...prog }
B: Helms Row / 1x12-20, 1x14-20 / 45lb @10+ 90s / superset: B / progress: custom() { ...prog }
B: Shoulder Press / 1x9-12, 1x6-12 / @9+ 120s / superset: C / progress: custom() { ...prog }
Seated Row / 1x17-20 77.5lb, 1x17-20 80lb / @10+ 90s / superset: C / progress: custom(increment: 2.5lb) { ...prog }

## Day 6 - Bro Day B
BroB: Hammer Curl / 1x12-20, 1x13-20 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
BroB: Triceps Extension, Cable / 1x15-15, 1x13-15 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
BroB: Bicep Curl / 1x10-12, 1x9-12 / @10+ 45s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
BroB: Triceps Pushdown / 1x8-15, 1x7-15 / @10+ 90s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
BroB: Lateral Raise / 1x13-20, 1x10-20 / @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Lu Lateral Raise / 2x10-15 / 10lb @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Cable Rear Delt One-Arm Row / 2x15-20 / 12.5lb @10+ 60s / progress: custom(increment: 2.5lb) { ...prog }
BroB: Neck Flexion / 1x4-20 / 3.5lb @10+ 30s / progress: custom(increment: 1lb) { ...prog }
BroB: Wrist Curl, Dumbbell / 1x14-20 / 24lb @10+ 30s / progress: custom(increment: 1lb) { ...prog }


# Week 6
## Day 1 - Legs A
Hack Squat, Smith Machine / 1x10-10, 1x13-15, 1x9-15 / @8+ 180s / progress: custom() { ...prog }
Stiff Leg Deadlift, Dumbbell / 1x11-15, 1x9-15 / @9+ 120s / progress: custom() { ...prog }
dpz: Walking Lunge / 2x12-30 / 15lb @10+ 120s / progress: custom() { ...prog }
dpz: Lying Leg Curl / 1x10-12, 1x12-12 / @10+ 90s / progress: custom() { ...prog }

## Day 2 - Torso A
Smith Machine Close Grip Larsen Press / 1x7-8 120lb, 2x5-8 130lb / @9+ 120s / superset: A / progress: custom() { ...prog }
Narrow: Narrow Pulldown / 1x10-15+ 97.5lb, 1x5-15+ 100lb, 1x3-15+ 100lb / @9+ 90s / superset: A / progress: custom() { ...prog }
Smith Reverse Grip Bench / 1x9-12, 1x7-12 / 90lb @9+ 120s / superset: B / progress: custom() { ...prog }
Wide: Machine Pulldown / 1x13-15 135lb, 1x12-15 127.5lb / @9+ 90s / superset: B / progress: custom() { ...prog }
Cable Crossover / 1x11-15, 1x9-15 / 22.5lb @10+ 60s / superset: C / progress: custom(increment: 2.5lb) { ...prog }
Bent Over One Arm Row / 1x15-15 50lb, 1x9-15 / @10+ 120s / superset: C / progress: custom() { ...prog }
Pullover, Cable / 1x18-20 22.5lb, 1x14-20 27.5lb / @10+ 60s / progress: custom(increment: 2.5lb) { ...prog }

## Day 3 - Bro Day A
Hammer Curl / 1x10-20 25lb, 1x12-20 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
Triceps Pushdown / 1x12-15 60lb, 1x8-15 / @10+ 90s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
Incline Curl / 1x6-10 22lb, 1x6-10 / @10+ 60s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
Triceps Extension, Cable / 1x12-15, 1x14-15 / 47.5lb @10+ 90s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
dfd: Lateral Raise / 1x8-15, 1x10-15 / 26lb @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Upright Row / 1x13-20 25lb, 1x12-20 / @10+ 90s / progress: custom(increment: 2.5lb) { ...prog }

## Day 4 - Legs B
Squat, Smith Machine / 1x6-8, 1x5-8 / 130lb @9+ 210s / progress: custom() { ...prog }
Romanian Deadlift / 1x8-12, 1x5-12 / 70lb @9+ 120s / progress: custom() { ...prog }
Lying Leg Curl / 1x8-15 37.5lb, 1x8-15 / @10+ 90s / progress: custom() { ...prog }
Leg Extension / 1x13-20, 1x10-20 / @10+ 90s / progress: custom() { ...prog }
Standing Calf Raise, Barbell / 1x15-20 / 160lb @10+ 90s / progress: custom() { ...prog }

## Day 5 - Torso B
B: Bench Press, Dumbbell / 1x7-12, 1x9-12 / 70lb @9+ 120s / superset: A / progress: custom() { ...prog }
B: Machine Pulldown / 1x10-15, 1x8-15 / 130lb @10+ 90s / superset: A / progress: custom() { ...prog }
B: Chest Press, Leverage Machine / 2x9-12 / @9+ 120s / superset: B / progress: custom() { ...prog }
B: Helms Row / 1x12-20, 1x14-20 / 45lb @10+ 90s / superset: B / progress: custom() { ...prog }
B: Shoulder Press / 1x9-12, 1x6-12 / @9+ 120s / superset: C / progress: custom() { ...prog }
Seated Row / 1x17-20 77.5lb, 1x17-20 80lb / @10+ 90s / superset: C / progress: custom(increment: 2.5lb) { ...prog }

## Day 6 - Bro Day B
BroB: Hammer Curl / 1x12-20, 1x13-20 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
BroB: Triceps Extension, Cable / 1x15-15, 1x13-15 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
BroB: Bicep Curl / 1x10-12, 1x9-12 / @10+ 45s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
BroB: Triceps Pushdown / 1x8-15, 1x7-15 / @10+ 90s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
BroB: Lateral Raise / 1x13-20, 1x10-20 / @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Lu Lateral Raise / 2x10-15 / 10lb @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Cable Rear Delt One-Arm Row / 2x15-20 / 12.5lb @10+ 60s / progress: custom(increment: 2.5lb) { ...prog }
BroB: Neck Flexion / 1x4-20 / 3.5lb @10+ 30s / progress: custom(increment: 1lb) { ...prog }
BroB: Wrist Curl, Dumbbell / 1x14-20 / 24lb @10+ 30s / progress: custom(increment: 1lb) { ...prog }


# Week 7
## Day 1 - Legs A
Hack Squat, Smith Machine / 1x10-10, 1x13-15, 1x9-15 / @8+ 180s / progress: custom() { ...prog }
Stiff Leg Deadlift, Dumbbell / 1x11-15, 1x9-15 / @9+ 120s / progress: custom() { ...prog }
dpz: Walking Lunge / 2x12-30 / 15lb @10+ 120s / progress: custom() { ...prog }
dpz: Lying Leg Curl / 1x10-12, 1x12-12 / @10+ 90s / progress: custom() { ...prog }

## Day 2 - Torso A
Smith Machine Close Grip Larsen Press / 1x7-8 120lb, 2x5-8 130lb / @9+ 120s / superset: A / progress: custom() { ...prog }
Narrow: Narrow Pulldown / 1x10-15+ 97.5lb, 1x5-15+ 100lb, 1x3-15+ 100lb / @9+ 90s / superset: A / progress: custom() { ...prog }
Smith Reverse Grip Bench / 1x9-12, 1x7-12 / 90lb @9+ 120s / superset: B / progress: custom() { ...prog }
Wide: Machine Pulldown / 1x13-15 135lb, 1x12-15 127.5lb / @9+ 90s / superset: B / progress: custom() { ...prog }
Cable Crossover / 1x11-15, 1x9-15 / 22.5lb @10+ 60s / superset: C / progress: custom(increment: 2.5lb) { ...prog }
Bent Over One Arm Row / 1x15-15 50lb, 1x9-15 / @10+ 120s / superset: C / progress: custom() { ...prog }
Pullover, Cable / 1x18-20 22.5lb, 1x14-20 27.5lb / @10+ 60s / progress: custom(increment: 2.5lb) { ...prog }

## Day 3 - Bro Day A
Hammer Curl / 1x10-20 25lb, 1x12-20 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
Triceps Pushdown / 1x12-15 60lb, 1x8-15 / @10+ 90s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
Incline Curl / 1x6-10 22lb, 1x6-10 / @10+ 60s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
Triceps Extension, Cable / 1x12-15, 1x14-15 / 47.5lb @10+ 90s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
dfd: Lateral Raise / 1x8-15, 1x10-15 / 26lb @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Upright Row / 1x13-20 25lb, 1x12-20 / @10+ 90s / progress: custom(increment: 2.5lb) { ...prog }

## Day 4 - Legs B
Squat, Smith Machine / 1x6-8, 1x5-8 / 130lb @9+ 210s / progress: custom() { ...prog }
Romanian Deadlift / 1x8-12, 1x5-12 / 70lb @9+ 120s / progress: custom() { ...prog }
Lying Leg Curl / 1x8-15 37.5lb, 1x8-15 / @10+ 90s / progress: custom() { ...prog }
Leg Extension / 1x13-20, 1x10-20 / @10+ 90s / progress: custom() { ...prog }
Standing Calf Raise, Barbell / 1x15-20 / 160lb @10+ 90s / progress: custom() { ...prog }

## Day 5 - Torso B
B: Bench Press, Dumbbell / 1x7-12, 1x9-12 / 70lb @9+ 120s / superset: A / progress: custom() { ...prog }
B: Machine Pulldown / 1x10-15, 1x8-15 / 130lb @10+ 90s / superset: A / progress: custom() { ...prog }
B: Chest Press, Leverage Machine / 2x9-12 / @9+ 120s / superset: B / progress: custom() { ...prog }
B: Helms Row / 1x12-20, 1x14-20 / 45lb @10+ 90s / superset: B / progress: custom() { ...prog }
B: Shoulder Press / 1x9-12, 1x6-12 / @9+ 120s / superset: C / progress: custom() { ...prog }
Seated Row / 1x17-20 77.5lb, 1x17-20 80lb / @10+ 90s / superset: C / progress: custom(increment: 2.5lb) { ...prog }

## Day 6 - Bro Day B
BroB: Hammer Curl / 1x12-20, 1x13-20 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
BroB: Triceps Extension, Cable / 1x15-15, 1x13-15 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
BroB: Bicep Curl / 1x10-12, 1x9-12 / @10+ 45s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
BroB: Triceps Pushdown / 1x8-15, 1x7-15 / @10+ 90s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
BroB: Lateral Raise / 1x13-20, 1x10-20 / @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Lu Lateral Raise / 2x10-15 / 10lb @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Cable Rear Delt One-Arm Row / 2x15-20 / 12.5lb @10+ 60s / progress: custom(increment: 2.5lb) { ...prog }
BroB: Neck Flexion / 1x4-20 / 3.5lb @10+ 30s / progress: custom(increment: 1lb) { ...prog }
BroB: Wrist Curl, Dumbbell / 1x14-20 / 24lb @10+ 30s / progress: custom(increment: 1lb) { ...prog }


# Week 8
## Day 1 - Legs A
Hack Squat, Smith Machine / 1x10-10, 1x13-15, 1x9-15 / @8+ 180s / progress: custom() { ...prog }
Stiff Leg Deadlift, Dumbbell / 1x11-15, 1x9-15 / @9+ 120s / progress: custom() { ...prog }
dpz: Walking Lunge / 2x12-30 / 15lb @10+ 120s / progress: custom() { ...prog }
dpz: Lying Leg Curl / 1x10-12, 1x12-12 / @10+ 90s / progress: custom() { ...prog }

## Day 2 - Torso A
Smith Machine Close Grip Larsen Press / 1x7-8 120lb, 2x5-8 130lb / @9+ 120s / superset: A / progress: custom() { ...prog }
Narrow: Narrow Pulldown / 1x10-15+ 97.5lb, 1x5-15+ 100lb, 1x3-15+ 100lb / @9+ 90s / superset: A / progress: custom() { ...prog }
Smith Reverse Grip Bench / 1x9-12, 1x7-12 / 90lb @9+ 120s / superset: B / progress: custom() { ...prog }
Wide: Machine Pulldown / 1x13-15 135lb, 1x12-15 127.5lb / @9+ 90s / superset: B / progress: custom() { ...prog }
Cable Crossover / 1x11-15, 1x9-15 / 22.5lb @10+ 60s / superset: C / progress: custom(increment: 2.5lb) { ...prog }
Bent Over One Arm Row / 1x15-15 50lb, 1x9-15 / @10+ 120s / superset: C / progress: custom() { ...prog }
Pullover, Cable / 1x18-20 22.5lb, 1x14-20 27.5lb / @10+ 60s / progress: custom(increment: 2.5lb) { ...prog }

## Day 3 - Bro Day A
Hammer Curl / 1x10-20 25lb, 1x12-20 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
Triceps Pushdown / 1x12-15 60lb, 1x8-15 / @10+ 90s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
Incline Curl / 1x6-10 22lb, 1x6-10 / @10+ 60s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
Triceps Extension, Cable / 1x12-15, 1x14-15 / 47.5lb @10+ 90s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
dfd: Lateral Raise / 1x8-15, 1x10-15 / 26lb @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Upright Row / 1x13-20 25lb, 1x12-20 / @10+ 90s / progress: custom(increment: 2.5lb) { ...prog }

## Day 4 - Legs B
Squat, Smith Machine / 1x6-8, 1x5-8 / 130lb @9+ 210s / progress: custom() { ...prog }
Romanian Deadlift / 1x8-12, 1x5-12 / 70lb @9+ 120s / progress: custom() { ...prog }
Lying Leg Curl / 1x8-15 37.5lb, 1x8-15 / @10+ 90s / progress: custom() { ...prog }
Leg Extension / 1x13-20, 1x10-20 / @10+ 90s / progress: custom() { ...prog }
Standing Calf Raise, Barbell / 1x15-20 / 160lb @10+ 90s / progress: custom() { ...prog }

## Day 5 - Torso B
B: Bench Press, Dumbbell / 1x7-12, 1x9-12 / 70lb @9+ 120s / superset: A / progress: custom() { ...prog }
B: Machine Pulldown / 1x10-15, 1x8-15 / 130lb @10+ 90s / superset: A / progress: custom() { ...prog }
B: Chest Press, Leverage Machine / 2x9-12 / @9+ 120s / superset: B / progress: custom() { ...prog }
B: Helms Row / 1x12-20, 1x14-20 / 45lb @10+ 90s / superset: B / progress: custom() { ...prog }
B: Shoulder Press / 1x9-12, 1x6-12 / @9+ 120s / superset: C / progress: custom() { ...prog }
Seated Row / 1x17-20 77.5lb, 1x17-20 80lb / @10+ 90s / superset: C / progress: custom(increment: 2.5lb) { ...prog }

## Day 6 - Bro Day B
BroB: Hammer Curl / 1x12-20, 1x13-20 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
BroB: Triceps Extension, Cable / 1x15-15, 1x13-15 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
BroB: Bicep Curl / 1x10-12, 1x9-12 / @10+ 45s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
BroB: Triceps Pushdown / 1x8-15, 1x7-15 / @10+ 90s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
BroB: Lateral Raise / 1x13-20, 1x10-20 / @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Lu Lateral Raise / 2x10-15 / 10lb @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Cable Rear Delt One-Arm Row / 2x15-20 / 12.5lb @10+ 60s / progress: custom(increment: 2.5lb) { ...prog }
BroB: Neck Flexion / 1x4-20 / 3.5lb @10+ 30s / progress: custom(increment: 1lb) { ...prog }
BroB: Wrist Curl, Dumbbell / 1x14-20 / 24lb @10+ 30s / progress: custom(increment: 1lb) { ...prog }


# Week 9
## Day 1 - Legs A
Hack Squat, Smith Machine / 1x10-10, 1x13-15, 1x9-15 / @8+ 180s / progress: custom() { ...prog }
Stiff Leg Deadlift, Dumbbell / 1x11-15, 1x9-15 / @9+ 120s / progress: custom() { ...prog }
dpz: Walking Lunge / 2x12-30 / 15lb @10+ 120s / progress: custom() { ...prog }
dpz: Lying Leg Curl / 1x10-12, 1x12-12 / @10+ 90s / progress: custom() { ...prog }

## Day 2 - Torso A
Smith Machine Close Grip Larsen Press / 1x7-8 120lb, 2x5-8 130lb / @9+ 120s / superset: A / progress: custom() { ...prog }
Narrow: Narrow Pulldown / 1x10-15+ 97.5lb, 1x5-15+ 100lb, 1x3-15+ 100lb / @9+ 90s / superset: A / progress: custom() { ...prog }
Smith Reverse Grip Bench / 1x9-12, 1x7-12 / 90lb @9+ 120s / superset: B / progress: custom() { ...prog }
Wide: Machine Pulldown / 1x13-15 135lb, 1x12-15 127.5lb / @9+ 90s / superset: B / progress: custom() { ...prog }
Cable Crossover / 1x11-15, 1x9-15 / 22.5lb @10+ 60s / superset: C / progress: custom(increment: 2.5lb) { ...prog }
Bent Over One Arm Row / 1x15-15 50lb, 1x9-15 / @10+ 120s / superset: C / progress: custom() { ...prog }
Pullover, Cable / 1x18-20 22.5lb, 1x14-20 27.5lb / @10+ 60s / progress: custom(increment: 2.5lb) { ...prog }

## Day 3 - Bro Day A
Hammer Curl / 1x10-20 25lb, 1x12-20 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
Triceps Pushdown / 1x12-15 60lb, 1x8-15 / @10+ 90s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
Incline Curl / 1x6-10 22lb, 1x6-10 / @10+ 60s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
Triceps Extension, Cable / 1x12-15, 1x14-15 / 47.5lb @10+ 90s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
dfd: Lateral Raise / 1x8-15, 1x10-15 / 26lb @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Upright Row / 1x13-20 25lb, 1x12-20 / @10+ 90s / progress: custom(increment: 2.5lb) { ...prog }

## Day 4 - Legs B
Squat, Smith Machine / 1x6-8, 1x5-8 / 130lb @9+ 210s / progress: custom() { ...prog }
Romanian Deadlift / 1x8-12, 1x5-12 / 70lb @9+ 120s / progress: custom() { ...prog }
Lying Leg Curl / 1x8-15 37.5lb, 1x8-15 / @10+ 90s / progress: custom() { ...prog }
Leg Extension / 1x13-20, 1x10-20 / @10+ 90s / progress: custom() { ...prog }
Standing Calf Raise, Barbell / 1x15-20 / 160lb @10+ 90s / progress: custom() { ...prog }

## Day 5 - Torso B
B: Bench Press, Dumbbell / 1x7-12, 1x9-12 / 70lb @9+ 120s / superset: A / progress: custom() { ...prog }
B: Machine Pulldown / 1x10-15, 1x8-15 / 130lb @10+ 90s / superset: A / progress: custom() { ...prog }
B: Chest Press, Leverage Machine / 2x9-12 / @9+ 120s / superset: B / progress: custom() { ...prog }
B: Helms Row / 1x12-20, 1x14-20 / 45lb @10+ 90s / superset: B / progress: custom() { ...prog }
B: Shoulder Press / 1x9-12, 1x6-12 / @9+ 120s / superset: C / progress: custom() { ...prog }
Seated Row / 1x17-20 77.5lb, 1x17-20 80lb / @10+ 90s / superset: C / progress: custom(increment: 2.5lb) { ...prog }

## Day 6 - Bro Day B
BroB: Hammer Curl / 1x12-20, 1x13-20 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
BroB: Triceps Extension, Cable / 1x15-15, 1x13-15 / @10+ 60s / superset: A / progress: custom(increment: 2.5lb) { ...prog }
BroB: Bicep Curl / 1x10-12, 1x9-12 / @10+ 45s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
BroB: Triceps Pushdown / 1x8-15, 1x7-15 / @10+ 90s / superset: B / progress: custom(increment: 2.5lb) { ...prog }
BroB: Lateral Raise / 1x13-20, 1x10-20 / @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Lu Lateral Raise / 2x10-15 / 10lb @10+ 60s / progress: custom(increment: 1lb) { ...prog }
Cable Rear Delt One-Arm Row / 2x15-20 / 12.5lb @10+ 60s / progress: custom(increment: 2.5lb) { ...prog }
BroB: Neck Flexion / 1x4-20 / 3.5lb @10+ 30s / progress: custom(increment: 1lb) { ...prog }
BroB: Wrist Curl, Dumbbell / 1x14-20 / 24lb @10+ 30s / progress: custom(increment: 1lb) { ...prog }


# Week 10 - Deload
## Day 1 - Legs A
Hack Squat, Smith Machine / 1x10-10 / @8+ 180s / progress: none
Stiff Leg Deadlift, Dumbbell / 1x11-15 / @9+ 120s / progress: none
dpz: Walking Lunge / 1x12-30 / 15lb @10+ 120s / progress: none
dpz: Lying Leg Curl / 1x10-12 / @10+ 90s / progress: none

## Day 2 - Torso A
Smith Machine Close Grip Larsen Press / 1x7-8 / 130lb @9+ 120s / superset: A / progress: none
Narrow: Narrow Pulldown / 1x10-15+ / 100lb @9+ 90s / superset: A / progress: none
Smith Reverse Grip Bench / 1x9-12 / 90lb @9+ 120s / superset: B / progress: none
Wide: Machine Pulldown / 1x13-15 / 135lb @9+ 90s / superset: B / progress: none
Cable Crossover / 1x11-15 / 22.5lb @10+ 60s / superset: C / progress: none
Bent Over One Arm Row / 1x15-15 / 50lb @10+ 120s / superset: C / progress: none
Pullover, Cable / 1x18-20 / 22.5lb @10+ 60s / progress: none

## Day 3 - Bro Day A
Hammer Curl / 1x10-20 / 25lb @10+ 60s / superset: A / progress: none
Triceps Pushdown / 1x12-15 / 60lb @10+ 90s / superset: A / progress: none
Incline Curl / 1x6-10 / 22lb @10+ 60s / superset: B / progress: none
Triceps Extension, Cable / 1x12-15 / 47.5lb @10+ 90s / superset: B / progress: none
dfd: Lateral Raise / 1x8-15 / 26lb @10+ 60s / progress: none
Upright Row / 1x13-20 / 25lb @10+ 90s / progress: none

## Day 4 - Legs B
Squat, Smith Machine / 1x6-8 / 130lb @9+ 210s / progress: none
Romanian Deadlift / 1x8-12 / 70lb @9+ 120s / progress: none
Lying Leg Curl / 1x8-15 / 37.5lb @10+ 90s / progress: none
Leg Extension / 1x13-20 / @10+ 90s / progress: none
Standing Calf Raise, Barbell / 1x15-20 / 160lb @10+ 90s / progress: none

## Day 5 - Torso B
B: Bench Press, Dumbbell / 1x7-12 / 70lb @9+ 120s / superset: A / progress: none
B: Machine Pulldown / 1x10-15 / 130lb @10+ 90s / superset: A / progress: none
B: Chest Press, Leverage Machine / 1x9-12 / @9+ 120s / superset: B / progress: none
B: Helms Row / 1x12-20 / 45lb @10+ 90s / superset: B / progress: none
B: Shoulder Press / 1x9-12 / @9+ 120s / superset: C / progress: none
Seated Row / 1x17-20 / 80lb @10+ 90s / superset: C / progress: none

## Day 6 - Bro Day B
BroB: Hammer Curl / 1x12-20 / @10+ 60s / superset: A / progress: none
BroB: Triceps Extension, Cable / 1x15-15 / @10+ 60s / superset: A / progress: none
BroB: Bicep Curl / 1x10-12 / @10+ 45s / superset: B / progress: none
BroB: Triceps Pushdown / 1x8-15 / @10+ 90s / superset: B / progress: none
BroB: Lateral Raise / 1x13-20 / @10+ 60s / progress: none
Lu Lateral Raise / 1x10-15 / 10lb @10+ 60s / progress: none
Cable Rear Delt One-Arm Row / 1x15-20 / 12.5lb @10+ 60s / progress: none
BroB: Neck Flexion / 1x4-20 / 3.5lb @10+ 30s / progress: none
BroB: Wrist Curl, Dumbbell / 1x14-20 / 24lb @10+ 30s / progress: none
