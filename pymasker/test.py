from pymasker import qabmasker
from pymasker import confidence

masker = qabmasker(r'C:\Users\Yu\Desktop\a\LC80160302014185LGN00_BQA.TIF')
mask = masker.getmask(cloud = confidence.high,
					  cirrus = confidence.high,
					  veg = confidence.none,
					  snow = confidence.none,
					  water = confidence.none,
					  inclusive = False,
					  cumulative = False)
masker.savetif(mask, r'C:\Users\Yu\Desktop\aa.tif')