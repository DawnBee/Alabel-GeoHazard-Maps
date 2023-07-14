from django.core.files.storage import FileSystemStorage
import os

def add_linebreaks(elem):
    return elem.replace('\n','<br>')

def set_marker(marker):
    name = marker.name if hasattr(marker,"name") else None
    info = marker.info if hasattr(marker,"info") else None
    image = f"/media/{marker.image}"
    level = marker.level if hasattr(marker,"level") else None
    location = marker.location if hasattr(marker,"location") else None

    lvl_format = f"{level} Susceptibility"

    # Generate HTML pattern for the marker
    html = ""

    # Barangay Pattern
    if level is not None:
        html += f"<b><center><img src='{image}' height=150 width=150></center></b>"
        html += f"<b><center><h2>{name}</h2></center></b>"
        html += f"<b><center><h4>{lvl_format}</h4></center></b>"
        html += f"<p>{add_linebreaks(info)}</p>"

    
    # Warning Devices Pattern    
    elif location is not None and info is not None:
        html += f"<b><center><img src='{image}' height=150 width=150></center></b>"
        html += f"<b><center><h3>{name}</h3></center></b>"
        html += f"<b><center><small>{location}</small></center></b>"
        html += f"<b><p>{add_linebreaks(info)}</p></b>"

    # Evac and Signs Pattern   
    else:
        html += f"<b><center><img src='{image}' height=150 width=150></center></b>"
        html += f"<b><center><h3>{name}</h3></center></b>"
        html += f"<b><center><small>{location}</small></center></b>"

    return html

# Custom classes to handle choropleth map layers
class OverwriteStorage(FileSystemStorage):
    CHOROPLETH_PATH = "choropleth_storage"

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(self.CHOROPLETH_PATH, name))
        return name 

choropleth_storage = OverwriteStorage(location="choropleth_storage")    


class FloodFileRename:
    dirs = ['dynamic', 'flood_map']

    @classmethod
    def rename_to_low(cls, instance, filename):
        ext = filename.split('.')[-1]
        filename = "low_lvl.%s" % (ext)
        return os.path.join(cls.dirs[0],cls.dirs[1],filename)

    @classmethod
    def rename_to_mod(cls, instance, filename):
        ext = filename.split('.')[-1]
        filename = "mod_lvl.%s" % (ext)
        return os.path.join(cls.dirs[0],cls.dirs[1],filename)

    @classmethod
    def rename_to_high(cls, instance, filename):
        ext = filename.split('.')[-1]
        filename = "high_lvl.%s" % (ext)
        return os.path.join(cls.dirs[0],cls.dirs[1],filename)

    @classmethod
    def rename_to_very_high(cls, instance, filename):
        ext = filename.split('.')[-1]
        filename = "very_high_lvl.%s" % (ext)
        return os.path.join(cls.dirs[0],cls.dirs[1],filename)


class LandslideFileRename:
    dirs = ['dynamic', 'landslide_map']

    @classmethod
    def rename_to_low(cls, instance, filename):
        ext = filename.split('.')[-1]
        filename = "low_lvl.%s" % (ext)
        return os.path.join(cls.dirs[0],cls.dirs[1],filename)

    @classmethod
    def rename_to_mod(cls, instance, filename):
        ext = filename.split('.')[-1]
        filename = "mod_lvl.%s" % (ext)
        return os.path.join(cls.dirs[0],cls.dirs[1],filename)

    @classmethod
    def rename_to_high(cls, instance, filename):
        ext = filename.split('.')[-1]
        filename = "high_lvl.%s" % (ext)
        return os.path.join(cls.dirs[0],cls.dirs[1],filename)

    @classmethod
    def rename_to_very_high(cls, instance, filename):
        ext = filename.split('.')[-1]
        filename = "very_high_lvl.%s" % (ext)
        return os.path.join(cls.dirs[0],cls.dirs[1],filename)        

class MapInfo:
    @staticmethod
    def info(lvl):
        storage = choropleth_storage
        verbose_name= f"{lvl.capitalize()} Risk Map"
        help_text= f"Note: Make sure you uploaded the correct '{verbose_name}' file before confirming changed."

        results = [storage,verbose_name,help_text]  
        return results    