from django.test import TestCase
from oembed.core import replace

class OEmbedTests(TestCase):
    end = ur"There is this great video at %s"
    start = ur"%s is a video that I like."
    middle = ur"There is a movie here: %s and I really like it."
    trailing_comma = ur"This is great %s, but it might not work."
    trailing_period = ur"I like this video, located at %s."
    
    noembeds = (
        ur"This is text that should not match any regex.",
        ur'<img src="http://i243.photobucket.com/albums/ff105/Kiyoko_Otani/Mokona.jpg" border="0" alt="MOKONA! Pictures, Images and Photos">',
        ur'<a rel="nofollow" href="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/alleXsumi.jpg"><img width="240" height="320" style="border:1px solid #000000;" src="http://img.photobucket.com/albums/v195/Alexiel-sama/AnimeNEXT09/alleXsumi.jpg"></a>',
    )
    embeds = (
        (u"http://www.viddler.com/explore/SYSTM/videos/49/", u'<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="320" height="222" id="viddlerplayer-e5cb3aac"><param name="movie" value="http://www.viddler.com/player/e5cb3aac/" /><param name="allowScriptAccess" value="always" /><param name="wmode" value="transparent" /><param name="allowFullScreen" value="true" /><embed src="http://www.viddler.com/player/e5cb3aac/" width="320" height="222" type="application/x-shockwave-flash" wmode="transparent" allowScriptAccess="always" allowFullScreen="true" name="viddlerplayer-e5cb3aac" ></embed></object>'),
        (u"http://www.flickr.com/photos/33312563@N05/3510704966/", u'<img src="http://farm4.staticflickr.com/3641/3510704966_45cccdd80c_m.jpg" alt="9"></img>'),
    )
    
    def testNoEmbed(self):
        for noembed in self.noembeds:
            self.assertEquals(
                replace(noembed),
                noembed
            )
    
    def testNoEmbedSpeed(self):
        for noembed in self.noembeds * 100:
            replace(noembed)
    
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
     
    
    