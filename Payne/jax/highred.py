import jax.numpy as np
from astropy.io import ascii

class highAv(object):
    """docstring for highAv"""
    def __init__(self, filters):
        super(highAv, self).__init__()

        AvTab = self.Avdata()

        self.Avlist = []

        for ff in filters:
            if ff in AvTab['filter']:
                AvTab_i = AvTab[AvTab['filter'] == ff]
                self.Avlist.append([AvTab_i['a1'][0],AvTab_i['b1'][0],AvTab_i['a2'][0],AvTab_i['b2'][0],AvTab_i['c2'][0]])
            else:
                self.Avlist.append([np.nan,np.nan,np.nan,np.nan,np.nan])

    def getAvaprox(self,Av,Rv,pars):
        a1,b1,a2,b2,c2 = pars
        return a1 + b1 * Av * (a2 + b2 * Rv + c2 * Rv**2.0)  

    def calc(self,BC0,Av,Rv):
        offset = [self.getAvaprox(Av,Rv,pars_i) for pars_i in self.Avlist]
        return np.array([BC0_i - offset_i for offset_i,BC0_i in zip(offset,BC0)])


    def Avdata(self,):
        datastr = (
        """
        filter a1 b1 a2 b2 c2
        2MASS_H 0.005144743611935593 -0.08825804196965176 -4.459177107383617 1.3211410779710815 -0.126433306346117
        2MASS_J 0.005440139230159183 -0.23220874507059025 -2.9976731151290528 0.9214433960096281 -0.09029532801360127
        2MASS_Ks 0.002080727108144654 -0.12514127988737334 -1.9538876061688348 0.594465850222952 -0.05813606611952772
        Bessell_B 0.024026662865963402 -0.32742482625331054 -5.0101650007947285 0.5122639727388698 -0.046816477985748846
        Bessell_I 0.00608032720073613 -0.3649990760906186 -3.0372850482808205 0.7326438817961413 -0.07162932318768075
        Bessell_R 0.03687149748433364 -0.14548310063602554 -6.847739151725625 0.764136666546879 -0.07078756454293482
        Bessell_U 0.011068394305864133 -0.8471523538338936 -2.9767563900443217 0.5359552511836281 -0.05176193472112856
        Bessell_V 0.012743463425026642 -0.3196046543375275 -3.179566963010358 0.026123205537807507 -0.0003117061154394677
        DECam_g 0.04115712676056599 -0.30487088780209165 -4.367925491769426 0.30241680199346616 -0.02783930321229807
        DECam_i 0.007747733390556156 -0.35225044719391024 -3.1031049661142895 0.7082956629043371 -0.06907632739455859
        DECam_r 0.017595577279324974 -0.31860259533916185 -3.0618144563482472 0.2727699090763789 -0.025561143811902432
        DECam_u 0.252666185225621 -0.3278280427724266 -6.138639988717908 1.1124745460602294 -0.10830144392927668
        DECam_Y 0.005504701666350007 -0.5365591678584216 -1.879253187564485 0.5645672977662803 -0.05495564940087354
        DECam_z 0.0031451859083615596 -0.5758231012970472 -1.8552400559111628 0.5308557206056973 -0.05155285771311707
        GaiaEDR3_BP 0.055854215903599645 -0.7972043730881687 -1.3894760033719158 0.06616276289549072 -0.005857153221577319
        GaiaEDR3_G 0.12057203687932089 -0.2525227913427648 -4.336001947381523 0.720204558822844 -0.06805098620541307
        GaiaEDR3_RP 0.02946290477315579 -0.24781923920815546 -4.271789759856738 0.9442627909930771 -0.09007769339862141
        PS_g 0.02619481275668664 -0.25473207898451533 -5.066162472416731 0.27256103863529985 -0.02498316555972354
        PS_i 0.008490793245946367 -0.2980911132560113 -3.5758213315082257 0.7299319701673537 -0.07051900668523702
        PS_open 0.09878720311534951 -0.32375162504359306 -3.349665862678733 0.6866680566351743 -0.06567610439795757
        PS_r 0.01243703788072692 -0.2200685494613116 -4.357785544339804 0.26879907111520207 -0.025655859926055475
        PS_w 0.0741790114713694 -0.27779886910872215 -3.8695032534101528 0.5591042210719966 -0.05285657309301058
        PS_y 0.0009783524686903554 -0.5411068745004978 -1.900255764099841 0.5608815063012451 -0.05435325320638657
        PS_z 0.006483935234238692 -0.42559299082994645 -2.545467678698392 0.6785248863926562 -0.06527716454160742
        SDSS_g 0.030171691981168158 -0.3510024963702352 -3.956685220715426 0.2810288871084623 -0.02611804408969654
        SDSS_i 0.00934772453074893 -0.3064794771046136 -3.4619644122798037 0.6943329304978475 -0.06685179624157737
        SDSS_r 0.018633709572431857 -0.21284999189323806 -4.43653353563524 0.2216952600605888 -0.02054924206900492
        SDSS_u 0.0016098529011755844 -0.8801717353090474 -2.9462277119780387 0.5460873781655091 -0.05322650499439604
        SDSS_z 0.003194414394289341 -0.5979742561551475 -1.7873365613016978 0.4946532251812435 -0.04779791192816546
        UKIDSS_H 0.004416004963041819 -0.19479812192073626 -2.1848121789581123 0.6817792963483705 -0.06781266315410932
        UKIDSS_J 0.004197098868485492 -0.2128514084967593 -3.1467656000328055 0.9532308115988369 -0.0921528016729265
        UKIDSS_K 0.0014310573374417522 -0.13309431471654487 -1.799949356549422 0.5537930415179917 -0.05433187126458154
        UKIDSS_Y 0.004982315345173704 -0.5092746294785129 -1.8874057609957313 0.5763660440620139 -0.05603635635634214
        UKIDSS_Z -0.0008063445246205867 -0.5779479437405286 -1.8820887983705692 0.5203086310059224 -0.05061507998058623
        WISE_W1 0.0011136720232548332 -0.03877027338553681 -2.9583239165256305 0.9281557214778126 -0.09137963142879639
        WISE_W2 0.0008618909401068488 -0.02703054946991242 -2.287398644395039 0.7033087429181879 -0.06893019357993094
        WISE_W3 0.0009575866429145087 -0.0035105268029923162 -1.8984841432336566 -0.07669755406322497 0.06367380243588723
        WISE_W4 -0.00018545908549038855 -0.07050330992020402 -0.023811954726825825 0.0019668778940036807 -9.754409334329754e-08
        SPHx_0 -0.001346300727468143 -0.293811607746542 -3.646973279398847 0.7591650611211381 -0.0736888343828133
        SPHx_1 0.0009852816297770183 -0.32949823582270255 -3.300185570050249 0.7406347638623559 -0.07252739394333443
        SPHx_2 -0.0006105644409070133 -0.3686568745886678 -2.991603844164958 0.7140224525634159 -0.06985237130694136
        SPHx_3 0.002648301280096852 -0.4033971835742945 -2.7207554713499 0.6722580249090435 -0.0652068956350763
        SPHx_4 0.004368465726952271 -0.5859374502755709 -1.902003720879967 0.49464526745477666 -0.04817085494388631
        SPHx_5 5.9832334568234356e-05 -0.45400056764081553 -2.4184259309537284 0.644423875057556 -0.06261676009386002
        SPHx_6 -0.0005234460186856578 -0.6029874127658369 -1.8201727749207097 0.5016886952469426 -0.04879462585125128
        SPHx_7 -0.0005332447330054331 -0.5790880776494665 -1.8735071654903892 0.527676328347358 -0.051214360199327326
        SPHx_8 0.00012090377796071574 -0.5781475043746545 -1.8592411438650502 0.5353532778846325 -0.05184356947652793
        SPHx_9 -0.0008474223990813977 -0.5492461962087309 -1.920127676998712 0.5638720239034302 -0.054867708976224186
        SPHx_10 -6.558736634392065e-05 -0.5397595745394664 -1.8981012631672467 0.5602743559478964 -0.053984443815466056
        SPHx_11 -0.00039421796418693774 -0.5764509205166729 -1.737497168162332 0.5223970439919302 -0.05077576413415622
        SPHx_12 -0.00038948664411594616 -0.5357679452016484 -1.8091156136528255 0.544198186901185 -0.05255773717751187
        SPHx_13 0.0012995332819307687 -0.5881680643736942 -1.5984700715687055 0.4859790046062633 -0.047208083455677854
        SPHx_14 0.0005355277019579513 -0.4633605664290309 -1.9664774236891265 0.6034288930913316 -0.05899991095756856
        SPHx_15 0.0003547228978751997 -0.3503482782217229 -2.475896494877949 0.7541999922679193 -0.0731028066038529
        SPHx_16 -1.7937144426505704e-06 -0.2650949605649761 -3.1497039700268474 0.9637063335703742 -0.09354681666836923
        SPHx_17 0.003978568988114281 -0.3042702069665025 -2.653550285765283 0.8153624755208576 -0.07929411427561928
        SPHx_18 0.004349089265960314 -0.24278204924380056 -3.1800341319070595 0.9753193307226649 -0.09481546583337389
        SPHx_19 -0.0003641701377601216 -0.27640044788166956 -2.6011812122853426 0.7845511370842596 -0.07565578780403923
        SPHx_20 0.002559927485157219 -0.2339822298030132 -2.983208782972547 0.9132548119720812 -0.0894522314982492
        SPHx_21 0.0006249115894232705 -0.2489485344803927 -2.6707581960648645 0.8186300229956879 -0.08036923982156256
        SPHx_22 0.0034043383280925846 -0.2666746584782975 -2.3840462396854023 0.7235632537106976 -0.07020240523404842
        SPHx_23 0.001951944581922427 -0.14952822577472466 -4.077256790687903 1.2431629583528694 -0.12107056911886038
        SPHx_24 0.004484674536190464 -0.08340226630774497 -6.944110898280986 2.106078931621568 -0.20438855027313227
        SPHx_25 -0.0011720512748658305 -0.1519610222610875 -3.6061199416895184 1.0866292339798032 -0.10538022480470538
        SPHx_26 0.006386645219979959 -0.25471354160412446 -2.101159732173294 0.6448610516406355 -0.06332412929792695
        SPHx_27 0.004083853227929984 -0.07644613791539734 -6.696312475623754 2.050244697748254 -0.20062516278572776
        SPHx_28 0.006042721489478305 -0.11316578828911379 -4.278896844350392 1.301797680986768 -0.12648397814899637
        SPHx_29 0.00230397964649084 -0.18200205068127914 -2.5596650349140813 0.7805717768041333 -0.07615556073112723
        SPHx_30 0.0031387138794272294 -0.09735205866788597 -4.614096812527501 1.4182234817043093 -0.13947540951507648
        SPHx_31 0.0036205577329803903 -0.14172511058036574 -3.0557990484104005 0.9342339569600011 -0.09089048034783981
        SPHx_32 0.003023887791294427 -0.1985355700925882 -2.071223855011195 0.6388548428669903 -0.0626017433540565
        SPHx_33 0.0023678661557124396 -0.21317996308047035 -1.841436976353983 0.5660210173902452 -0.055470248959635614
        SPHx_34 0.004215832187764391 -0.10414212735404758 -3.7058494815108904 1.142606585567382 -0.11204865659443214
        SPHx_35 0.0023762915879874556 -0.129911884522171 -2.816563263383856 0.8547995014665468 -0.08296938776293879
        SPHx_36 0.004177311591613509 -0.10073580859282072 -3.513569844363591 1.0761962173845432 -0.10514051316395351
        SPHx_37 0.0025731048178560772 -0.09409856144471636 -3.592233515380153 1.1152909885665556 -0.11019347498097805
        SPHx_38 0.0027641065809332526 -0.09338930523311022 -3.4451328825241663 1.0461568244698347 -0.1017293220856923
        SPHx_39 0.002861426567425393 -0.11015875816486656 -2.7982979713570812 0.8618186784933934 -0.08432873449477353
        SPHx_40 0.002224908661054973 -0.08256272755773544 -3.5474101356025693 1.0927297077592868 -0.10728251274080432
        SPHx_41 0.0019372839232832213 -0.14794449733053716 -1.9202005054781486 0.5869858620901953 -0.05727115684481825
        SPHx_42 0.002135432313736008 -0.13688581769939326 -1.9492079319189497 0.5981924703721745 -0.058735947496156356
        SPHx_43 0.0036860956589904867 -0.1336436449942661 -1.9355891049267042 0.5919775512140754 -0.057461022851392256
        SPHx_44 0.002038329656856524 -0.1334312309081138 -1.842436572983885 0.5615800905902194 -0.054798020910543935
        SPHx_45 0.002489994634414777 -0.12266870876324319 -1.9269813683954697 0.5956174822909653 -0.05879899885098464
        SPHx_46 0.0029819383925167348 -0.1224615029428438 -1.8639529853025678 0.5759941105665564 -0.056289805970971885
        SPHx_47 0.0018144177457235704 -0.07323285196742792 -2.981864643089312 0.9200954760443741 -0.08996836709797865
        SPHx_48 0.0004164030630820181 -0.10554256487068123 -1.9825797841503994 0.6166624429860857 -0.06098578153521846
        SPHx_49 0.0021498644665938257 -0.06395680307128936 -3.0503723021788525 0.9276246769357536 -0.0901449248127651
        SPHx_50 0.0005233168821916996 -0.11471508547504075 -1.6724433437464172 0.5135687618514263 -0.0505012711466531
        SPHx_51 0.002042810243670057 -0.06257380060000255 -2.9826959593273137 0.9039430921941863 -0.08699569011531369
        SPHx_52 0.004311043261069308 -0.09727913911130248 -1.7571507284047798 0.5353165733120915 -0.052638141637777296
        SPHx_53 0.001620149302320077 -0.05686737517903943 -2.9363654544732856 0.9030969771468536 -0.08819826539527695
        SPHx_54 0.0016498525746048505 -0.0917050018305094 -1.7033363212277242 0.5145185825440435 -0.0498114340138784
        SPHx_55 0.0016558294022899238 -0.09144139228180274 -1.698948164176564 0.5276879720764972 -0.052306898377977216
        SPHx_56 0.0013749621017964757 -0.08965764307954459 -1.5960957972613636 0.4920268220151794 -0.04806532611602036
        SPHx_57 0.0015562493196369309 -0.07774760530870782 -1.7105184509422935 0.5153075015106162 -0.05014187122037039
        SPHx_58 0.0007308305075242041 -0.04302989218948531 -3.0070992603949693 0.9012656003733375 -0.0868212800072246
        SPHx_59 -0.0011180754855647757 -0.04487671445221184 -2.77064878237407 0.9218565346802968 -0.1013692016021988
        SPHx_60 0.00020722383744481418 -0.07038486636563997 -1.6446445684681414 0.5007161375494086 -0.04890514344877872
        SPHx_61 -0.006030835207052781 -0.08712522608242779 -1.4775337515988398 0.5516844454442448 -0.06477301177384448
        SPHx_62 0.0009881678548875768 -0.06814737204395463 -1.5257964745645134 0.45329968864660747 -0.04353149714090859
        SPHx_63 0.0005648836788503897 -0.0348924209916506 -2.916635234494478 0.9007441606878405 -0.088594903198929
        SPHx_64 0.0013966603678059288 -0.06442286823100472 -1.5151896014235955 0.48120265138984747 -0.04844037805460042
        SPHx_65 0.0009142985566254564 -0.05583463567694838 -1.6000359310958807 0.48722327638030044 -0.047604715620985914
        SPHx_66 0.0007871628081060471 -0.055012043258196475 -1.5469272316983331 0.47548591824987524 -0.046642208482991866
        SPHx_67 0.0011620752208291083 -0.02535579975376146 -2.995563752643822 0.8953932715576293 -0.09072183816017176
        SPHx_68 0.00030387798113873404 -0.06073817201259769 -1.4003789831196718 0.42737156687118477 -0.04170510280319751
        SPHx_69 0.003318281309654864 -0.036602322935169775 -2.0018489706297995 0.5456233523227783 -0.04731039806459121
        SPHx_70 0.0005596428984121901 -0.0583110550074897 -1.1614084204797412 0.29048804744450396 -0.023846216021228307
        SPHx_71 0.0029328689275916996 -0.03296942848579184 -2.289321882523872 0.6532375391872443 -0.05928818965610022
        SPHx_72 0.00033301130112834397 -0.055700038533776815 -1.400293040549311 0.4284763042707743 -0.04202757484029649
        SPHx_73 0.0008581688371206015 -0.05332807437311138 -1.4505815735227428 0.4340187166812741 -0.04139787637665427
        SPHx_74 0.002190959241200242 -0.053233022905242844 -1.2536530378320005 0.3491134546773968 -0.03257180388331905
        SPHx_75 0.0017184087613061052 -0.024774764847861102 -2.9420262846708565 0.8866435734011798 -0.08492778537433324
        SPHx_76 0.0005615448672942029 -0.02547906720047332 -2.8637649486631207 0.8847981903322818 -0.08736140671955883
        SPHx_77 0.0009895722604923356 -0.03714047140616068 -1.9015318306846072 0.5752966538270141 -0.05475826114569535
        SPHx_78 0.000816152767507558 -0.03569454906766574 -2.00547617452869 0.6165601102674124 -0.06011913601432522
        SPHx_79 0.0010071917049949222 -0.03749617170290134 -1.893219553050965 0.5787268672508116 -0.05667093888732724
        SPHx_80 0.0010320855877220061 -0.03535514352704249 -1.8879153711467898 0.5686257513428072 -0.055270990193529296
        SPHx_81 0.00216366737158287 -0.052886984999750836 -1.106140098849303 0.3061927388170132 -0.028893750472015964
        SPHx_82 0.0006732365978610671 -0.03696708214037371 -1.7923453089889525 0.5762459678841438 -0.06093769325237598
        SPHx_83 0.0002811010058123176 -0.03454354988824821 -1.8683772713667943 0.5647560885051949 -0.05441650907133601
        SPHx_84 0.0004760037251993516 -0.03515832905371998 -1.789528055323876 0.537965280655786 -0.051775281871970356
        SPHx_85 -0.0035917343900356475 -0.03125164932915348 -2.3389215752063848 0.8799431165313566 -0.10373370728302828
        SPHx_87 0.0006505495595783025 -0.03370313235434314 -1.799243906549407 0.5322686674945507 -0.05104692532280764
        SPHx_88 0.0013751463763957243 -0.028995117916829873 -1.7920392163183712 0.4734390907722927 -0.04112418846673852
        SPHx_89 0.0003901435028862373 -0.03329867641031823 -1.783241113536067 0.5439936950681706 -0.0528866355717716
        SPHx_90 0.0014903720292379005 -0.06301364716246453 -0.8836419868232968 0.25589857348871453 -0.0239604284690564
        SPHx_92 0.0016690001356476148 -0.06266356140398377 -0.8926055235902418 0.27071954529408176 -0.026661870650032525
        SPHx_93 -0.002885014900158741 -0.031024647426350523 -2.0873875451541015 0.7519840198125648 -0.08738026085101934
        SPHx_94 0.0022629316776155285 -0.053419083505782713 -0.974188975651168 0.27164850962048703 -0.023928777245289398
        SPHx_96 -0.003443637687838836 -0.05549202353996754 -1.190585485584773 0.4489779717588418 -0.05264422037352448
        SPHx_97 0.002768173684883976 -0.02274471615953562 -2.058022492047431 0.517498977817445 -0.04228954463508172
        SPHx_98 0.0003804973567148103 -0.0298599163773671 -1.792105150495709 0.5427111933357914 -0.05278717842759762
        SPHx_100 0.0004492253000990919 -0.02896850292749007 -1.7800177964262884 0.5399907232944063 -0.05208190481910195
        SPHx_101 0.001320218040498955 -0.051630027338149774 -0.9995063541757665 0.3112076773036463 -0.03167672958143132"""
        )
        return ascii.read(datastr)