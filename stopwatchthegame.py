# template for "Stopwatch: The Game"

# define global variables
import simplegui
time = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    pass
    
# define event handlers for buttons; "Start", "Stop", "Reset"


# define event handler for timer with 0.1 sec interval
def tick():
    global time
    time += 1

# define draw handler
def draw(canvas):
    canvas.draw_text(str(time), [150, 150], 48, "red")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 300, 300)
frame.set_draw_handler(draw)

# register event handlers
timer = simplegui.create_timer(100, tick)

# start frame
frame.start()
timer.start()
# Please remember to review the grading rubric
