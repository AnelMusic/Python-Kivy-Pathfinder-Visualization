from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock

import config

import grid
import pathfinder

class MyApp(App):
    def build(self):
        return MyGrid()


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        #root = Widget()
        self.cols = 1
        self.TARGET_NODE_SET = False
        self.START_NODE_SET = False
        self.ALGORITHM_SET = False

        self.start_node = None
        self.target_node = None
        self.path_tuples = []
        self.path = []
        self.dynamic_id_dict = {}
        self.algorithm = -1
        self.num_buttons_clicked = 0
        self.num_wall_buttons_clicked = 0
        self.map_wall_list = []
        self.left_wall_elements = config.MAX_WALLELEMENTS

        self.initGui()
        self.info_label.text = "Set Wall Elements   ["+str(self.left_wall_elements)+"] left"
        #self.submit_btn = Button(text = "Submit",  size_hint=(1, None))
        #self.add_widget(self.submit_btn)

    def pressed(self, instance):
        if self.left_wall_elements >= 0:
            self.left_wall_elements -=1
            self.info_label.text = "Set Wall Elements   [" + str(self.left_wall_elements) + "] left"

            if self.left_wall_elements == 0:
                self.info_label.text = "Set Start Node"

        if self.num_wall_buttons_clicked == config.MAX_WALLELEMENTS:
            self.START_NODE_SET = True
            self.info_label.text = "Set Target Node"

            if (self.num_buttons_clicked == 0):
                instance.background_color = config.startnode_color
                self.start_node = instance.id
            elif (self.num_buttons_clicked == 1):
                instance.background_color = config.targetnode_color
                self.target_node = instance.id
                self.TARGET_NODE_SET = True
                self.info_label.text = "Select Algorithm"


            elif (self.num_buttons_clicked == 2):
                # routine to set all buttons
                # for i in range(len(self.dynamic_id_dict)):
                #    self.dynamic_id_dict[i].disabled = True
                pass
                #self.find_path()
            self.num_buttons_clicked+=1
        else:
            instance.background_color =config.btn_clicked_color
            instance.disabled = True
            self.num_wall_buttons_clicked+=1

            #problem dass dass dieses dictionary nicht meinem format entspricht
            # greife auf index zu, dabei ist es jetzt ein dictionary
            # einfach in die Map die id reinhauen
            self.map_wall_list.append(instance.id)
            print("[DEBUG] WALL BUTTON =    ", instance.id)

    # 2 Possible Events: Start button clicked or Clear button clicked
    def top_menue_pressed(self, instance):
        print("[DEBUG] BUTTON =    ", instance.id)
        if instance.id == "start_btn":
            if self.START_NODE_SET == True and self.TARGET_NODE_SET and self.ALGORITHM_SET:
                self.info_label.text = "Planner is searching for Target Node"
                world_grid = grid.Grid((self.map_layout.rows , self.map_layout.cols), self.map_wall_list)
                pf = pathfinder.Pathfinder(world_grid, self.map_wall_list, self.start_node, self.target_node)

                #Astar
                if self.algorithm == config.ALGORITHM_ASTAR:
                    self.path, self.closed_set = pf.find_path_astar()
                    if self.path:
                        Clock.schedule_interval(self.update_exploration_field, config.update_exploration_rate)
                    else:
                        Clock.schedule_interval(self.update_exploration_field, config.update_exploration_rate)
                #Bidirectional Dijkstra
                if self.algorithm == config.ALGORITHM_BIDIRECTIONAL_DIJKSTRA:
                    self.path, self.closed_set = pf.find_path_bidirect_dijkstra()
                    print("LEN PATH ? ", len(self.path))
                    for node in self.path:
                        print("Path:   ", node.position)

                    if self.path:
                        Clock.schedule_interval(self.update_exploration_field, config.update_exploration_rate)
                    else:
                        Clock.schedule_interval(self.update_exploration_field, config.update_exploration_rate)

                # DFS
                if self.algorithm == config.ALGORITHM_DFS:
                    #todo: wrong implementation
                    self.path, self.closed_set = pf.find_path_dfs()
                    print("FINAL_VIS STAACK LEN = ", len(self.closed_set))
                    for i in self.closed_set:
                        print("Closed set node: ", i.position)
                    if self.path:
                        Clock.schedule_interval(self.update_exploration_field, config.update_exploration_rate)
                    #else:
                    #    Clock.schedule_interval(self.update_exploration_field, config.update_exploration_rate)
                # BFS
                if self.algorithm == config.ALGORITHM_BFS:
                    # todo: Implement Algorithm
                    self.path, self.closed_set = pf.find_path_bfs()

                    for node in self.path:
                        print("___ path ____ ", node.position)


                    if self.path:
                        Clock.schedule_interval(self.update_exploration_field, config.update_exploration_rate)
                    else:
                        Clock.schedule_interval(self.update_exploration_field, config.update_exploration_rate)



            else:
                print("CANT START PLANNER")
        elif instance.id == "clear_btn":
            self.reset()

    # Handle reset event
    def reset(self):
        for node in self.dynamic_id_dict:
            print(node)
            self.dynamic_id_dict[node].background_color = config.node_color
            self.dynamic_id_dict[node].disabled = False
        self.TARGET_NODE_SET = False
        self.START_NODE_SET = False
        self.start_node = None
        self.target_node = None
        self.path_tuples = []
        self.num_buttons_clicked = 0
        self.num_wall_buttons_clicked = 0
        self.map_wall_list = []
        self.path = []
        self.left_wall_elements = config.MAX_WALLELEMENTS
        self.info_label.text = "Set Wall Elements   ["+str(self.left_wall_elements)+"] left"

    #handle dropdown events
    def drop_down_pressed(self, instance):
        print("Instance ID ", instance.id)
        if instance.id == "dropdown_astar":
            self.ALGORITHM_SET = True
            self.algorithm = config.ALGORITHM_ASTAR
            self.info_label.text = "Start Planner"
        if instance.id == "dropdown_dijkstra":
            self.ALGORITHM_SET = True
            self.algorithm = config.ALGORITHM_DIJKSTRA
            self.info_label.text = "Start Planner"
        if instance.id == "dropdown_dfs":
            self.ALGORITHM_SET = True
            self.algorithm = config.ALGORITHM_DFS
            self.info_label.text = "Start Planner"
        if instance.id == "dropdown_bfs":
            self.ALGORITHM_SET = True
            self.algorithm = config.ALGORITHM_BFS
            self.info_label.text = "Start Planner"
        if instance.id == "dropdown_gbfs":
            self.ALGORITHM_SET = True
            self.algorithm = config.ALGORITHM_GBFS
            self.info_label.text = "Start Planner"
        if instance.id == "dropdown_bdijkstra":
            self.ALGORITHM_SET = True
            self.algorithm = config.ALGORITHM_BIDIRECTIONAL_DIJKSTRA
            self.info_label.text = "Start Planner"

    #Create UI and Setup Map
    def initGui(self):
        # Top Menue
        self.top_menue_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)

        algo_btn = Button(id="algo_btn", on_press=self.top_menue_pressed, text="Algorithm", font_name='DejaVuSans',
                          background_color=config.btn_color)
        self.top_menue_layout.add_widget(algo_btn)
        start_btn = Button(id="start_btn", text="Start Pathfinder", on_press=self.top_menue_pressed,
                           font_name='DejaVuSans', background_color=config.btn_color)
        self.top_menue_layout.add_widget(start_btn)
        clear_btn = Button(id="clear_btn", text="Clear Map", on_press=self.top_menue_pressed,
                           font_name='DejaVuSans', background_color=config.btn_color)  # r g b 91/255,96/255,107/255,255/255
        self.top_menue_layout.add_widget(clear_btn)

        # Sub Menue
        self.sub_menue_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=30)
        self.info_label = Label(id="info_label", text="Info Text", font_name='DejaVuSans')
        self.sub_menue_layout.add_widget(self.info_label)

        # Map ( BtnMap)
        self.map_layout = GridLayout()
        self.map_layout.cols = 15
        self.map_layout.rows = 15

        for i in range(self.map_layout.cols * self.map_layout.rows):
            # remapping from index to x,y id
            x = int(i / self.map_layout.cols)
            y = i % self.map_layout.cols
            string_id = "(" + str(x) + ", " + str(y) + ")"

            #           button = Button(text=str(i),
            button = Button(id=string_id,
                            # size_hint=(None, None),   remove the wrong size
                            on_press=self.pressed, background_color=config.node_color)

            self.map_layout.add_widget(button)

            self.dynamic_id_dict.update({string_id: button})

        #Dropdown Btns for Algorithm Btn
        dropdown = DropDown()
        btn_astar = Button(text="AStar", id = "dropdown_astar",on_press=self.drop_down_pressed,size_hint_y=None, height=44, font_name='DejaVuSans', background_color=[280/255, 280/255, 280/ 225, 1])
        btn_astar.bind(on_release=lambda btn: dropdown.select(btn.text))
        dropdown.add_widget(btn_astar)
        algo_btn.bind(on_release=dropdown.open)
        btn_astar = Button(text="Dijkstra's",id = "dropdown_dijkstra", on_press=self.drop_down_pressed,size_hint_y=None, height=44, font_name='DejaVuSans', background_color=[280/255, 280/255, 280/ 225, 1])
        btn_astar.bind(on_release=lambda btn: dropdown.select(btn.text))
        dropdown.add_widget(btn_astar)
        algo_btn.bind(on_release=dropdown.open)
        btn_astar = Button(text="Depth-First_Search",id = "dropdown_dfs",on_press=self.drop_down_pressed, size_hint_y=None, height=44, font_name='DejaVuSans', background_color=[280/255, 280/255, 280/ 225, 1])
        btn_astar.bind(on_release=lambda btn: dropdown.select(btn.text))
        dropdown.add_widget(btn_astar)
        algo_btn.bind(on_release=dropdown.open)
        btn_astar = Button(text="Breadth-First_Search",id = "dropdown_bfs",on_press=self.drop_down_pressed, size_hint_y=None, height=44, font_name='DejaVuSans', background_color=[280/255, 280/255, 280/ 225, 1])
        btn_astar.bind(on_release=lambda btn: dropdown.select(btn.text))
        dropdown.add_widget(btn_astar)
        algo_btn.bind(on_release=dropdown.open)
        btn_astar = Button(text="Greedy-Best-First_Search",id = "dropdown_gbfs",on_press=self.drop_down_pressed, size_hint_y=None, height=44, font_name='DejaVuSans', background_color=[280/255, 280/255, 280/ 225, 1])
        btn_astar.bind(on_release=lambda btn: dropdown.select(btn.text))
        dropdown.add_widget(btn_astar)
        algo_btn.bind(on_release=dropdown.open)
        btn_astar = Button(text="Bidirection Dijkstra",id = "dropdown_bdijkstra",on_press=self.drop_down_pressed, size_hint_y=None, height=44, font_name='DejaVuSans', background_color=[280/255, 280/255, 280/ 225, 1])
        btn_astar.bind(on_release=lambda btn: dropdown.select(btn.text))
        dropdown.add_widget(btn_astar)
        algo_btn.bind(on_release=dropdown.open)

        # one last thing, listen for the selection in the dropdown list and
        # assign the data to the button text.
        dropdown.bind(on_select=lambda instance, x: setattr(algo_btn, 'text', x))
        self.add_widget(self.top_menue_layout)
        self.add_widget(self.sub_menue_layout)
        self.add_widget(self.map_layout)

    def update_path_field(self, arg):
        if len(self.path) > 0:
            self.dynamic_id_dict[str(self.path[-1].position)].background_color = config.final_path_color
            self.path.pop(-1)
            if len(self.path) == 0:
                Clock.unschedule(self.update_path_field)

    def update_exploration_field(self, arg):
        print("NOT DONE")
        if len(self.closed_set) > 0:
            if str(self.closed_set[0].position) != self.target_node \
                    and str(self.closed_set[0].position) != self.start_node:
                self.dynamic_id_dict[str(self.closed_set[0].position)].background_color = config.exploration_color
            self.closed_set.pop(0)

            #workaround in order to trigger the path_update_method
            # todo explain workaround a bit more in detail
            # Kivy clock shit

            if len(self.closed_set) == 0:
                print("DONE")
                Clock.unschedule(self.update_exploration_field)
                Clock.schedule_interval(self.update_path_field, config.update_path_rate)
