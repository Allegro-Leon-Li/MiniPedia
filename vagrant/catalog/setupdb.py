from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Category, CategoryItem, User


engine = create_engine('sqlite:///catalogwithuser.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

User1 = User(name="Leon li", email="ec.leonli@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')  # noqa
session.add(User1)
session.commit()


cat1 = Category(user_id=1, name="Nature")
it1 = CategoryItem(user_id=1, name="Oceans",
                   description="An ocean is a major body of saline water, and a principal component of the hydrosphere. Approximately 71\% of the Earth's surface (an area of some 361 million square kilometers) is covered by ocean, a continuous body of water that is customarily divided into several principal oceans and smaller seas. More than half of this area is over 3,000 meters (9,800 feet) deep. Average oceanic salinity is around 35 parts per thousand (ppt) (3.5\%), and nearly all seawater has a salinity in the range of 30 to 38 ppt. Though generally recognized as several 'separate' oceans, these waters comprise one global, interconnected body of salt water often referred to as the World Ocean or global ocean. This concept of a global ocean as a continuous body of water with relatively free interchange among its parts is of fundamental importance to oceanography.", category=cat1)
it2 = CategoryItem(user_id=1, name="Lakes",
                   description="A lake (from Latin lacus) is a terrain feature (or physical feature), a body of liquid on the surface of a world that is localized to the bottom of basin (another type of landform or terrain feature; that is, it is not global) and moves slowly if it moves at all. On Earth, a body of water is considered a lake when it is inland, not part of the ocean, is larger and deeper than a pond, and is fed by a river. The only world other than Earth known to harbor lakes is Titan, Saturn's largest moon, which has lakes of ethane, most likely mixed with methane. It is not known if Titan's lakes are fed by rivers, though Titan's surface is carved by numerous river beds. Natural lakes on Earth are generally found in mountainous areas, rift zones, and areas with ongoing or recent glaciation. Other lakes are found in endorheic basins or along the courses of mature rivers. In some parts of the world, there are many lakes because of chaotic drainage patterns left over from the last Ice Age. All lakes are temporary over geologic time scales, as they will slowly fill in with sediments or spill out of the basin containing them.", category=cat1)
it3 = CategoryItem(user_id=1, name="Plant", description="Plants are mainly multicellular, predominantly photosynthetic eukaryotes of the kingdom Plantae. The term is today generally limited to the green plants, which form an unranked clade Viridiplantae (Latin for 'green plants'). This includes the flowering plants, conifers and other gymnosperms, ferns, clubmosses, hornworts, liverworts, mosses and the green algae, and excludes the red and brown algae. Historically, plants formed one of two kingdoms covering all living things that were not animals, and both algae and fungi were treated as plants; however all current definitions of 'plant' exclude the fungi and some algae, as well as the prokaryotes (the archaea and bacteria).", category=cat1)
it4 = CategoryItem(user_id=1, name="Animal", description="Animals are eukaryotic, multicellular organisms that form the biological kingdom Animalia. With few exceptions, animals are motile (able to move), heterotrophic (consume organic material); they reproduce sexually, and their embryonic development includes a blastula stage. The body plan of the animal derives from this blastula, developing specialized tissues and organs as it develops; this plan eventually becomes fixed, although some undergo metamorphosis at some stage in their lives.", category=cat1)
session.add(cat1)
session.add(it1)
session.add(it2)
session.add(it3)
session.add(it4)
session.commit()

cat1 = Category(user_id=1, name="History")
it1 = CategoryItem(user_id=1, name="Renaissance", description="The Renaissance was a period in European history, from the 14th to the 17th century, regarded as the cultural bridge between the Middle Ages and modern history. It started as a cultural movement in Italy in the Late Medieval period and later spread to the rest of Europe, marking the beginning of the Early Modern Age.", category=cat1)
it2 = CategoryItem(user_id=1, name="World War II", description="World War II (often abbreviated to WWII or WW2), also known as the Second World War, was a global war that lasted from 1939 to 1945, although related conflicts began earlier. It involved the vast majority of the world's countries including all of the great powers eventually forming two opposing military alliances, the Allies and the Axis. It was the most widespread war in history, and directly involved more than 100 million people from over 30 countries. In a state of total war, the major participants threw their entire economic, industrial, and scientific capabilities behind the war effort, erasing the distinction between civilian and military resources.", category=cat1)
it3 = CategoryItem(user_id=1, name="Silk Road",
                   description="The Silk Road or Silk Route was an ancient network of trade routes that were for centuries central to cultural interaction originally through regions of Eurasia connecting the East and West and stretching from the Korean peninsula and Japan to the Mediterranean Sea. The Silk Road concept refers to both the terrestrial and the maritime routes connecting Asia and Europe. The overland Steppe route stretching through the Eurasian steppe is considered the ancestor to the Silk Road(s).", category=cat1)
session.add(cat1)
session.add(it1)
session.add(it2)
session.add(it3)
session.commit()

cat1 = Category(user_id=1, name="Science")
it1 = CategoryItem(user_id=1, name="Force",
                   description="In physics, a force is any interaction that, when unopposed, will change the motion of an object. A force can cause an object with mass to change its velocity (which includes to begin moving from a state of rest), i.e., to accelerate. Force can also be described intuitively as a push or a pull. A force has both magnitude and direction, making it a vector quantity. It is measured in the SI unit of newtons and represented by the symbol F.", category=cat1)
it2 = CategoryItem(user_id=1, name="Metal", description="A metal is a material (an element, compound, or alloy) that is typically hard, opaque, shiny, and has good electrical and thermal conductivity. Metals are generally malleable that is, they can be hammered or pressed permanently out of shape without breaking or cracking as well as fusible (able to be fused or melted) and ductile (able to be drawn out into a thin wire). About 91 of the 118 elements in the periodic table are metals; the others are nonmetals or metalloids. Some elements appear in both metallic and non metallic forms.", category=cat1)
it3 = CategoryItem(user_id=1, name="DNA", description="Deoxyribonucleic acid is a molecule that carries the genetic instructions used in the growth, development, functioning and reproduction of all known living organisms and many viruses. DNA and ribonucleic acid (RNA) are nucleic acids; alongside proteins, lipids and complex carbohydrates (polysaccharides), they are one of the four major types of macromolecules that are essential for all known forms of life. Most DNA molecules consist of two biopolymer strands coiled around each other to form a double helix.", category=cat1)
session.add(cat1)
session.add(it1)
session.add(it2)
session.add(it3)
session.commit()
