# Variables related to the achievement system itself
default achievements = [] # A list of all achievements
default achievement_notification_queue = [] # A list of achievements which the user will be shown a notification on

# Variables related to the achievement stat screen
default selected_achievement = False # Used for achievement screen to remember the last selected achievement
define achievement_categories = ['Exploration','Lewdness','Other']
define selected_category = [category.lower() for category in achievement_categories]
default show_unlocked_achievements = True
default show_locked_achievements = True
default show_hidden_achievements = False

### Achievements ###

# if persistent.achivement_cheat = True:
#     $ achievement_trophy_case.update()
#     $ achievement_all_the_stuff.update(16)
#     $ achievement_mc_finished.update()
#     $ achievement_even_more_wine.update(10)
#     $ achievement_all_the_wine.update(5)
#     $ achievement_wine_collector.update()
#     $ achievement_been_everywhere.update(13)
#     $ achievement_diverse_panties.update()
#     $ achievement_fs_panties_5.update(5)
#     $ achievement_fs_panties_1.update(1)
#     $ achievement_fs_panties_sniffer.update()

init 10:
    # A special achievement, which takes the place of any achievement when it is hidden
    default achievement_hidden = NewAchievement("???", "This achievement is hidden.\nPlay the game to figure out what it is", 1, 'gui/hidden.webp', register=False)

    # Other Achievements
    default achievement_trophy_case = NewAchievement("Trophy Case", "Open the achievement screen", 1, 'gui/star.webp')
    default achievement_all_the_stuff = NewAchievement("All the stuff","Find, and pick up, all the stuff in game",16,'gui/star.webp')
    default achievement_mc_finished = NewAchievement("Ace Mechanic","Finish rebuilding the bike",1,'gui/star.webp')
    default achievement_even_more_wine = NewAchievement("Even more wine!","That's 10 bottles. Please tell me you're not gonna drink them alone?",10,'inventory/wine_idle.webp',hidden=True)
    default achievement_all_the_wine = NewAchievement("All the wine!","That's 5 bottles. Please tell me you're not gonna drink them alone?",5,'inventory/wine_idle.webp',hidden=True,next_tier=[achievement_even_more_wine])
    default achievement_wine_collector = NewAchievement("Wine collector","You've aquired wine!",1,'inventory/wine_idle.webp',hidden=True,next_tier=[achievement_all_the_wine])

    # Exploration Achievements
    default achievement_been_everywhere = NewAchievement("Seasoned traveller","You visited every location in the game",13,'gui/star.webp','exploration')

    # Lewdness Achievements
    default achievement_diverse_panties = NewAchievement("Diverse Collector","One of every type!",1,'inventory/fsp_hot_pink_idle.webp','lewdness',True)
    default achievement_fs_panties_5 = NewAchievement("Collector","You're building a collection",5,'inventory/fsp_hot_pink_idle.webp','lewdness',True)
    default achievement_fs_panties_1 = NewAchievement("The start of a budding\ncollection...", "You're a perv! And you have panties!",1,'inventory/fsp_hot_pink_idle.webp','lewdness',True,next_tier=[achievement_fs_panties_5])
    default achievement_fs_panties_sniffer = NewAchievement("Panty sniffer", "You're a perv! And you have panties!",1,'inventory/fsp_hot_pink_idle.webp','lewdness',True)


init python:
    class NewAchievement(object):
        def __init__(self, name, description, progress_max, image_path, category='other', hidden=False, next_tier=False, register=True):
            global achievements
            self.name = name
            self.description = description
            self.unlocked = False
            self.progress = 0
            self.progress_max = progress_max
            self.image = "%s" % image_path
            self.category = category
            self.hidden = hidden
            self.hidden_image = "%s" % image_path
            self.next_tier = next_tier
            if register:
                achievements.append(self)
                # achievements.sort(key=lambda x: x.hidden)

        # Unlock this achievement and show the user a quick notification
        def unlock(self):
            if self.unlocked is False:
                self.hidden = False
                self.unlocked = True
                if len(achievement_notification_queue) > 0:
                    achievement_notification_queue.append(self)
                else:
                    achievement_notification_queue.append(self)
                    renpy.show_screen(_screen_name='display_achievement_unlocked')#, achievement_name=self.name, achievement_description=self.description, achievement_image=self.image)
                self.unhide_following_tier()

        def unhide(self):
            self.hidden = False
            # achievements.sort(key=lambda x: x.hidden)
            renpy.notify('An achievement is now visible\n%s' % self.name)

        def update(self, increment=1):
            if self.unlocked:
                return
            self.progress += increment
            if self.progress >= self.progress_max:
                self.progress = self.progress_max
                self.unlock()

        def unhide_following_tier(self):
            if self.next_tier:
                for achievement in self.next_tier:
                    achievement.unhide()

    def update_mc_achievement(mc_b=None,mc_f=False):
        if mc_b is not None:
            if mc_b == 150 and mc_f:
                achievement_mc_finished.update()

    def update_panties_achievements():
        if panties_sniffer:
            achievement_fs_panties_sniffer.update()
        if backpack.has_item(fsp_hot_pink_item) or backpack.has_item(fsp_black_item) or backpack.has_item(fsp_light_blue_item) or backpack.has_item(fsp_yellow_item) or backpack.has_item(fsp_red_item):
            achievement_fs_panties_1.update()
            achievement_fs_panties_5.update()
        if backpack.has_item(fsp_hot_pink_item) and backpack.has_item(fsp_black_item) and backpack.has_item(fsp_light_blue_item) and backpack.has_item(fsp_yellow_item) and backpack.has_item(fsp_red_item):
            achievement_diverse_panties.update()

    def update_been_everywhere_achievement():
        # if fp_bedroom_ach and fs_bedroom_ach and uhl_bathroom_ach and uhl_ach and entrance_ach and livingroom_ach and kitchen_ach and outside_ach and garage_ach and school_outside_ach and school_principal_office_ach and beach_ach:
        achievement_been_everywhere.update()

    def update_all_the_stuff():
        global beer_pickup, carkeys_pickup, fsp_hot_pink_pickup, fsp_light_blue_pickup, fsp_black_pickup, fsp_yellow_pickup, fsp_red_pickup, gin_pickup, phone_pickup, princessplug_pickup, roses_pickup, schoolbooks_pickup, smallkeys_pickup, toolbox_pickup, vodka_pickup, wallet_pickup, whiskey_pickup, wine_pickup
        if beer_pickup:
            achievement_all_the_stuff.update()
            beer_pickup = False
        if carkeys_pickup:
            achievement_all_the_stuff.update()
            carkeys_pickup = False
        if fsp_hot_pink_pickup:
            achievement_all_the_stuff.update()
            fsp_hot_pink_pickup = False
        if fsp_light_blue_pickup:
            achievement_all_the_stuff.update()
            fsp_light_blue_pickup = False
        if fsp_black_pickup:
            achievement_all_the_stuff.update()
            fsp_black_pickup = False
        if fsp_yellow_pickup:
            achievement_all_the_stuff.update()
            fsp_yellow_pickup = False
        if fsp_red_pickup:
            achievement_all_the_stuff.update()
            fsp_red_pickup = False
        if gin_pickup:
            achievement_all_the_stuff.update()
            gin_pickup = False
        if phone_pickup:
            achievement_all_the_stuff.update()
            phone_pickup = False
        if princessplug_pickup:
            achievement_all_the_stuff.update()
            princessplug_pickup = False
        if roses_pickup:
            achievement_all_the_stuff.update()
            roses_pickup = False
        if schoolbooks_pickup:
            achievement_all_the_stuff.update()
            schoolbooks_pickup = False
        if smallkeys_pickup:
            achievement_all_the_stuff.update()
            smallkeys_pickup = False
        if toolbox_pickup:
            achievement_all_the_stuff.update()
            toolbox_pickup = False
        if vodka_pickup:
            achievement_all_the_stuff.update()
            absolut_pickup = False
        if wallet_pickup:
            achievement_all_the_stuff.update()
            wallet_pickup = False
        if whiskey_pickup:
            achievement_all_the_stuff.update()
            whiskey_pickup = False
        if wine_pickup:
            achievement_all_the_stuff.update()
            wine_pickup = False