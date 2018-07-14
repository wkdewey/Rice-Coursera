# template for "Stopwatch: The Game"

# define global variables
import simplegui
time = 0
stopwatch_running = False
total_stops = 0
successes = 0
print str(successes)

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    a = t // 600
    seconds = (t // 10) % 60
    b = seconds // 10
    c = seconds % 10
    d = t % 10
    return str(a) + ":" + str(b) + str(c) + "." + str(d)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global stopwatch_running
    stopwatch_running = True
    timer.start()
    
def stop():
    global total_stops, successes, stopwatch_running
    timer.stop()
    if stopwatch_running == True:
        total_stops += 1
        if time % 10 == 0:
            successes += 1
    stopwatch_running = False
    
def reset():
    global time, successes, total_stops, stopwatch_running
    timer.stop()
    time = 0
    successes = 0
    total_stops = 0
    stopwatch_running = False

# define event handler for timer with 0.1 sec interval
def tick():
    global time
    time += 1

# define draw handler
def draw(canvas):
    counters = str(successes) + "/" + str(total_stops)
    canvas.draw_text(format(time), [100, 170], 48, "red")
    canvas.draw_text(counters, [200, 50], 48, "green")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 300, 300)

# register event handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, tick)
frame.add_button("Start", start)
frame.add_button("Stop", stop)
frame.add_button("Reset", reset)
# start frame
frame.start()
# Please remember to review the grading rubric
