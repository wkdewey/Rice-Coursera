"""
Cookie Clicker Simulator
"""

import simpleplot
import math
# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(200)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0
#SIM_TIME = 1000000
class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return ("Time: " + str(self._time) + " Current Cookies: " + str(self._current_cookies) + 
             " CPS: " + str(self._cps) + " Total Cookies: " + str(self._total_cookies))
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        history_list = list(self._history)
        return history_list

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies > self._current_cookies:
            time_remaining = math.ceil((cookies - self._current_cookies) / self._cps)
            return float(time_remaining)
        else:
            return 0.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._time = self._time + time
            self._current_cookies += (time*self._cps)
            self._total_cookies += (time*self._cps)
        else:
            return
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if (self._current_cookies - cost) >= 0:
            self._current_cookies -= cost
            self._cps += additional_cps
            print ("Bought item: " + str(item_name) + " Time: " + str(self._time) +
                   " Cookies: " + str(self._current_cookies) + " Cost: " + str(cost))
            self._history.append((self._time, item_name, cost, self._total_cookies))
        else:
            return
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    
    # Replace with your code
    build = build_info.clone()
    game = ClickerState()
    while game.get_time() <= duration:
        time_remaining = duration - game.get_time()
        item = strategy(game.get_cookies(), game.get_cps(), game.get_history(), time_remaining, build)
        if item == None:
            game.wait(time_remaining)
            return game
        item_cost = build.get_cost(item)
        time_to_wait = game.time_until(item_cost)
        if time_to_wait > time_remaining:
            game.wait(time_remaining)
            return game
        game.wait(time_to_wait)
        game.buy_item(item, item_cost, build.get_cps(item))
        build.update_item(item)
    return game


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    items = build_info.build_items()
    min_cost = cookies + cps * time_left
    cheapest = None
    for item in items:
        if build_info.get_cost(item) <= min_cost:
            min_cost = build_info.get_cost(item)
            cheapest = item
    if cheapest:
        return str(cheapest)
    else:
        print "none available"
        return None

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    items = build_info.build_items()
    max_cost = 0
    most_expensive = None
    cookies_available = cookies + cps * time_left
    for item in items:
        item_cost = build_info.get_cost(item)
        if item_cost >= max_cost and item_cost <= cookies_available:
            max_cost = item_cost
            most_expensive = item
    if most_expensive:
        return str(most_expensive)
    else:
        return None

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    items = build_info.build_items()
    max_efficiency = 0
    most_efficient = None
    cookie_threshold = cookies + cps * time_left
    for item in items:
        item_cost = build_info.get_cost(item)
        item_cps = build_info.get_cps(item)
        if item_cps/item_cost >= max_efficiency and item_cost <= cookie_threshold:
            max_efficiency = item_cps/item_cost
            most_efficient = item
    if most_efficient:
        return str(most_efficient)
    else:
        return None
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)
    #run_strategy("None", SIM_TIME, strategy_none)
    # Add calls to run_strategy to run additional strategies
    #run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
#run()
#print strategy_expensive(500000.0, 1.0, [(0.0, None, 0.0, 0.0)], 5.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15))
    

