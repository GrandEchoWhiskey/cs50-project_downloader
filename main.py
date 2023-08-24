from svn.remote import RemoteClient as SVNClient
import os

class Repo:
    def __init__(self, name, url):
        self.name = name
        self.url = url+"/trunk/"
        self.connection = SVNClient(self.url)

    def sub_dirs(self):
        ignore = ['data']
        return sorted([x for x in self.connection.list() if not ((x in map(lambda y: y+'/', ignore)) or ('.' in x))])
    
    def __str__(self):
        result = ""
        for id, name in enumerate(self.sub_dirs()):
            result += f"{id + 1}. {name.split('/')[0]}\n"
        return result
    
    def select(self, id):
        url = self.url + self.sub_dirs()[id - 1]
        return SVNClient(url)

class Repos():
    def __init__(self):
        self.current = None
        self.repos = [
            Repo("Harvard CS50x Projects", "https://github.com/GrandEchoWhiskey/harvard-cs50-x-projects"),
            Repo("Harvard CS50P Projects", "https://github.com/GrandEchoWhiskey/harvard-cs50-python-projects"),
            Repo("Harvard CS50AI Projects", "https://github.com/GrandEchoWhiskey/harvard-cs50-ai-projects"),
            Repo("Harvard CS50W Projects", "https://github.com/GrandEchoWhiskey/harvard-cs50-web-projects"),
            Repo("Harvard CS50G Projects", "https://github.com/GrandEchoWhiskey/harvard-cs50-game-projects")
        ]

    def select(self, id):
        print(f"Selected: {self.repos[id - 1].name}")
        self.current = self.repos[id - 1]

    def __str__(self):
        result = ""
        for id, obj in enumerate(self.repos):
            result += f"{id + 1}. {obj.name}\n"
        return result

dir_path = os.path.dirname(os.path.realpath(__file__))

print(Repos())
repos = Repos()
if selection := input("Select: "):
    if selection.isnumeric():
        repos.select(int(selection))
        print(repos.current)
        if selection := input("Select: "):
            if selection.isnumeric() and int(selection) <= len(repos.current.sub_dirs()):
                print(f"Selected: {repos.current.sub_dirs()[int(selection) - 1]}")
                print(f"Exporting to {dir_path}/{repos.current.sub_dirs()[int(selection) - 1]}")
                repos.current.select(int(selection)).export(dir_path + "/" + repos.current.sub_dirs()[int(selection) - 1])
                print("Done!")
            else:
                print("Invalid Selection")
    else:
        print("Invalid Selection")