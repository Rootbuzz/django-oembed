from django.test import TestCase
from django.template.defaultfilters import safe
from oembed.core import replace, fetch
from oembed.models import StoredOEmbed, ProviderRule

class OEmbedTests(TestCase):
    end = ur"There is this great video at %s"
    start = ur"%s is a video that I like."
    middle = ur"There is a movie here: %s and I really like it."
    trailing_comma = ur"This is great %s, but it might not work."
    trailing_period = ur"I like this video, located at %s."
    
    noembeds = (
        ur"This is text that should not match any regex.",
        u'<img src="http://i243.photobucket.com/albums/ff105/Kiyoko_Otani/Mokona.jpg" border="0" alt="MOKONA! Pictures, Images and Photos">',
        u'<a rel="nofollow" href="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/alleXsumi.jpg"><img width="240" height="320" style="border:1px solid #000000;" src="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/alleXsumi.jpg"></a>',
        u'blah blah <a href="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam00group_best2.jpg"><img width="320" height="240" style="border:1px solid #000000;" src="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam00group_best2.jpg" /></a> blah',
        u'''
            <p>If anyone went to AnimeNEXT 09, then maybe you saw four Season 1 Gundam 00 Meisters in a group wandering around together. This was a group that I organized and kept everyone accounted for. I'm thankful to have had such dedicated people making my first serious cosplay experience an enjoyable one. If you didn't see us this year, then look for us next year hopefully. 
            </p>
            <p>For the record, these pics were taken from other Gundam cosplayers, not using my camera. I also really want to find the shot taken of Tieria and Lockon kissing. XD For now, enjoy the pics and the awesomeness thereof!
            </p>
            <ul>
             <li>
                 Setsuna F. Seiei (red scarf): Nina (ALEX)
             </li>
            
             <li>
                 Allelujah Haptism/Hallelujah: KOU (my illustrator)
             </li>
            
             <li>
                 Tieria Erde: Sasha
             </li>
            
             <li>
                 Lockon Stratos: jim
             </li>
            </ul>
            <p><a href="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam00group_best2.jpg"><img width="320" height="240" style="border:1px solid #000000;" src="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam00group_best2.jpg" /></a> <a href="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/setsunashot.jpg"><img width="320" height="240" style="border:1px solid #000000;" src="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/setsunashot.jpg" /></a>
            </p>
            <p><a href="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/alleXsumi.jpg"><img width="240" height="320" style="border:1px solid #000000;" src="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/alleXsumi.jpg" /></a> <a href="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam00group.jpg"><img width="320" height="240" style="border:1px solid #000000;" src="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam00group.jpg" /></a>
            </p>
            <p><a href="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam00group2.jpg"><img width="320" height="240" style="border:1px solid #000000;" src="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam00group2.jpg" /></a> <a href="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam00group3.jpg"><img width="320" height="240" style="border:1px solid #000000;" src="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam00group3.jpg" /></a>
            </p>
            <p><a href="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam00group4.jpg"><img width="320" height="240" style="border:1px solid #000000;" src="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam00group4.jpg" /></a> <a href="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam00group5.jpg"><img width="320" height="240" style="border:1px solid #000000;" src="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam00group5.jpg" /></a>
            </p>
            <p><a href="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam00group6.jpg"><img width="320" height="240" style="border:1px solid #000000;" src="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam00group6.jpg" /></a> <a href="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam00group_best.jpg"><img width="320" height="240" style="border:1px solid #000000;" src="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam00group_best.jpg" /></a>
            </p>
            <p><a href="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam_cosplay_shoot_best.jpg"><img width="320" height="240" style="border:1px solid #000000;" src="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/gundam_cosplay_shoot_best.jpg" /></a> 
            </p>
            <p>By the way, if anyone can recommend how to go about washing my outfit, I'd love to know so I don't shrink/ruin it orz.
            </p>
        '''
    )
    embeds = (
        (u"http://www.viddler.com/explore/SYSTM/videos/49/", u'<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="320" height="222" id="viddlerplayer-e5cb3aac"><param name="movie" value="http://www.viddler.com/player/e5cb3aac/" /><param name="allowScriptAccess" value="always" /><param name="wmode" value="transparent" /><param name="allowFullScreen" value="true" /><embed src="http://www.viddler.com/player/e5cb3aac/" width="320" height="222" type="application/x-shockwave-flash" wmode="transparent" allowScriptAccess="always" allowFullScreen="true" name="viddlerplayer-e5cb3aac" ></embed></object>'),
        (u"http://www.flickr.com/photos/33312563@N05/3510704966/", u'<img src="http://farm4.staticflickr.com/3641/3510704966_45cccdd80c_m.jpg" alt="9"></img>'),
    )
    
    def testNoEmbed(self):        
        fetch_count = fetch.count
        for noembed in self.noembeds:
            self.assertEquals(replace(noembed), noembed)
            self.assertEquals(replace(safe(noembed)), noembed)
        self.assertEquals(fetch_count, fetch.count)
    
    def testEnd(self):
        for text in (self.end, self.start, self.middle, self.trailing_comma, self.trailing_period):
            for loc, embed in self.embeds:
                self.assertEquals(
                    replace(text % loc),
                    text % embed
                )
    
    def testManySameEmbeds(self):
        for loc, embed in self.embeds:
            text = " ".join([self.middle % loc] * 100) 
            resp = " ".join([self.middle % embed] * 100)
            self.assertEquals(replace(text), resp)
        
    def testAlreadyEmbedded(self):
        for loc, embed in self.embeds:
            self.assertEquals(replace(embed), embed)
     
    
    