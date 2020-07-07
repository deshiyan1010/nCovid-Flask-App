import nltk 
import json
from fuzzywuzzy import fuzz
from nltk.stem import WordNetLemmatizer
import copy
from districtData import districtwise_info_dist
from plot_single import get_table
from zone_info import zone_info_fun_dis
import pandas as pd



def tokenizer(sentence):
    sentence = sentence.lower()
    tokens = nltk.word_tokenize(sentence)
    return tokens

def chat():

    states = ['Total India', 'Andaman and Nicobar Islands', 'Andra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli', 'Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']

    # districts = ['A.R. Nagar', 'Adat', 'Adichanallur', 'Adilabad', 'Adimali', 'Adoor', 'Agali', 'Agar Malwa', 'Agartala', 'Agra', 'Ahmedabad', 'Ahmednagar', 'Aikkaranad', 'Ajmer', 'Ajnala', 'Akalakunnam', 'Akathethara', 'Akola', 'Ala', 'Alackode', 'Alagappanagar', 'Alakkode', 'Alanallur', 'Alangad', 'Alankode', 'Alapadambu', 'Alappad', 'Alappuzha', 'Alathur', 'Alayamon', 'Aligarh', 'Aliparamba', 'Alipurduar', 'Alirajpur', 'Allahabad', 'Aloor', 'Aluva', 'Alwar', 'Amarambalam', 'Ambalappara', 'Ambalappuzha', 'Ambalavayal', 'Amballoor', 'Ambalppuzha', 'Amboori', 'Ampati', 'Amravati', 'Amritsar', 'Anakkara', 'Anakkayam', 'Ananganadi', 'Anchal', 'Andoorkonam', 'Angadippuram', 'Angamaly', 'Anikad', 'Anjarakandi', 'Annamanada', 'Anthikkad', 'Anthoor', 'Anuppur', 'Arakulam', 'Arakuzha', 'Aralam', 'Aranmula', 'Arattupuzha', 'Areacode', 'Arikkulam', 'Ariyalur', 'Arookutty', 'Aroor', 'Arpookkara', 'Aruvappulam', 'Aryad', 'Aryankavu', 'Aryankode', 'Ashok Nagar', 'Asifabad', 'Assamannoor', 'Athavanad', 'Athirampuzha', 'Athiyannoor', 'Atholi', 'Attingal', 'Aurangabad', 'Avanoor', 'Avoly', 'Ayancheri', 'Ayarkunnam', 'Ayavana', 'Ayilur', 'Aymanam', 'Ayroor', 'Ayyampuzha', 'Ayyankunnu', 'Ayyappancovil', 'Azhikode', 'Azhiyur', 'Azhoor', 'Baba Bakala', 'Baghmara', 'Baghpat', 'Baksa', 'Balaghat', 'Balod', 'Baloda Bazar', 'Balrampur', 'Balussery', 'Bambolim', 'Bangalore', 'Banswara', 'Baran', 'Barmer', 'Barpeta', 'Barwani', 'Bastar', 'Bathery', 'Belgaum', 'Bellary', 'Bemetara', 'Bengaluru', 'Berhampore', 'Betul', 'Bhadradri Kothagudem', 'Bharananganam', 'Bharanikkavu', 'Bharatpur', 'Bhavnagar', 'Bhayander', 'Bhilwara', 'Bhind', 'Bhopal', 'Bhubaneswar', 'Bhupalpally', 'Bidar', 'Bihar Sharif', 'Bikaner', 'Bilaspur', 'Biswanath', 'Bokaro', 'Bongaigaon', 'Boudh', 'Budhanoor', 'Bulandshahar', 'Bundi', 'Burhanpur', 'Bysonvalley', 'Cachar', 'Chadayamangalam', 'Chakkittappara', 'Chakkupallam', 'Chalakudy', 'Chalisserri', 'Chaliyar', 'Champakulam', 'Chandigarh', 'Changanacherry', 'Changaroth', 'Chapparapadavu', 'Charaideo', 'Chathamangalam', 'Chathannur', 'Chavakkad', 'Chavara', 'Chazhoor', 'Cheekode', 'Chekkyad', 'Chelannur', 'Chelembra', 'Chellanam', 'Chembilode', 'Chemencherry', 'Chemmaruthi', 'Chendamangalam', 'Chengalai', 'Chengalpattu', 'Chengamanade', 'Chengannur', 'Chengottukavu', 'Chenkal', 'Chennai', 'Chennam Pallippuram', 'Chennerkara', 'Chennithala', 'Cheppad', 'Cheranalloor', 'Cheriyamundam', 'Cheriyanad', 'Cherppalasseri', 'Cherpu', 'Cherthala', 'Cherukavu', 'Cherukol', 'Cherukunnu', 'Cherunniyoor', 'Cherupuzha', 'Cheruthana', 'Cheruthazham', 'Cheruvannur', 'Chettikulangara', 'Chhatarpur', 'Chheharta', 'Chhindwara', 'Chingoli', 'Chinnakanal', 'Chirakkadavu', 'Chirakkal', 'Chirakkara', 'Chirang', 'Chirayinkeezhu', 'Chithara', 'Chittar', 'Chittariparamb', 'Chittattukara', 'Chittorgarh', 'Chittur ULB', 'Chogawan', 'Chokkad', 'Chokli', 'Choondal', 'Choornikkara', 'Chorode', 'Chowannur', 'Chunakkara', 'Chungathara', 'Churu', 'Clappana', 'Coimbatore', 'Cuddalore', 'Cuttack', 'Cyberabad', 'Damoh', 'Dantewada', 'Darbhanga', 'Darrang', 'Datia', 'Dausa', 'Dehradun', 'Delhi', 'Deoghar', 'Desamangalam', 'Devikulam', 'Devikulangara', 'Dewas', 'Dhamtari', 'Dhanbad', 'Dhankheti', 'Dhar', 'Dharmadam', 'Dharmapuri', 'Dhemaji', 'Dholpur', 'Dhubri', 'Dhule', 'Dibrugarh', 'Dima Hasao', 'Dindori', 'Dindugul', 'Dungarpur', 'East Garo Hills', 'East Jaintia Hills', 'Edachery', 'Edakkara', 'Edakkattuvayal', 'Edamulakkal', 'Edapatta', 'Edappal', 'Edarikode', 'Edathala', 'Edathiruthi', 'Edathua', 'Edavaka', 'Edavanakkad', 'Edavanna', 'Edavetty', 'Edavilangu', 'Edayur', 'Elakamon', 'Elamadu', 'Elamkulam', 'Elamkunnapuzh.', 'Elampalloor', 'Elanji', 'Elanthoor', 'Elappara', 'Elapully', 'Elavally', 'Elavanchery', 'Elikulam', 'Eloor', 'Enadimangalam', 'Engandiyoor', 'Eramala', 'Eramam', 'Eranjoli', 'Erath', 'Erattupetta', 'Eraviperoor', 'Erimayur', 'Eriyad', 'Erode', 'Eroor', 'Erumely', 'Eruthenpathy', 'Eruvessi', 'Ettumanoor', 'Ezhamkulam', 'Ezhikkara', 'Ezhome', 'Ezhukone', 'Ezhumattoor', 'Ezhupunna', 'Faridabad', 'Faridkot', 'Feroke', 'Gadwal', 'Ganganagar', 'Gangtok', 'Ghaziabad', 'Goalpara', 'Golaghat', 'Goniana', 'Gorakhpur', 'Grp Ajmer', 'Grp Jodhpur', 'Gulbarga', 'Guna', 'Gurgaon', 'Guruvayur', 'Guwahati', 'Guwahati City', 'Gwalior', 'Hailakandi', 'Haldwani', 'Hamirpur', 'Hamren', 'Hanumangarh', 'Harda', 'Haripad', 'Hassan', 'Hazaribagh', 'Hojai', 'Hoshangabad', 'Hoshiarpur', 'Howrah', 'Hubli–Dharwad', 'Hyderabad', 'Imphal', 'Indore', 'Irikkur', 'Irimbiliyam', 'Irinjalakkuda', 'Iritty', 'Ittiva', 'Jabalpur', 'Jagdalpur', 'Jagtial', 'Jaipur', 'Jaipur Rural', 'Jaisalmer', 'Jalna', 'Jalore', 'Jammu', 'Jamnagar', 'Jamshedpur', 'Janagoan', 'Jandiala Guru', 'Jangaon', 'Janjgir', 'Jayashankar Bhupalapally', 'Jehanabad', 'Jhabua', 'Jhalawar', 'Jhunjhunu', 'Jhunjhunuu', 'Jodhpur', 'Jodhpur Rural', 'Jogulamba Gadwal', 'Jorhat', 'Jowai', 'Kabirdham', 'Kadakkal', 'Kadakkarapally', 'Kadakkavoor', 'Kadalundi', 'Kadamakkudy', 'Kadamakudy', 'Kadambazhippuram', 'Kadambur', 'Kadampanad', 'Kadanadu', 'Kadangod', 'Kadannapalli', 'Kadapa', 'Kadaplamattom', 'Kadapra', 'Kadavallur', 'Kadinamkulam', 'Kadukutty', 'Kaduthuruthy', 'Kainakary', 'Kaiparambu', 'Kaippamangalam', 'Kakinada', 'Kakkodi', 'Kakkur', 'Kaladi', 'Kalady', 'Kalamassery', 'Kalanjoor', 'Kalikavu', 'Kallakurichi', 'Kallara', 'Kalliassery', 'Kallikkadu', 'Kalloopara', 'Kalloorkkad', 'Kalluvathukkal', 'Kalpakanchery', 'Kalpetta', 'Kalyan-Dombivli', 'Kamareddy', 'Kamrup', 'Kanakkary', 'Kancheepuram', 'Kanchiyar', 'Kandalloor', 'Kandanassery', 'Kangazha', 'Kangra', 'Kanichar', 'Kaniyambetta', 'Kanjikuzhi', 'Kanjiramkulam', 'Kanjirappally', 'Kanjirappuzha', 'Kanjoor', 'Kannadi', 'Kannamangalam', 'Kannambra', 'Kannapuram', 'Kannur', 'Kanthaloor', 'Kanyakumari', 'Kappur', 'Karakurissi', 'Karalam', 'Karassery', 'Karauli', 'Karavaloor', 'Karavaram', 'Karbi Anglong', 'Kareepra', 'Karimannoor', 'Karimba', 'Karimganj', 'Karimnagar', 'Karimpuzha', 'Karinkunnam', 'Karivellur Peralam', 'Karode', 'Karoor', 'Karthikapally', 'Karukachal', 'Karulai', 'Karumalloor', 'Karumkulam', 'Karunagappally', 'Karunapuram', 'Karur', 'Karuvarakund', 'Karuvatta', 'Kasaragod', 'Katghora', 'Kathirur', 'Katni', 'Kattakambal', 'Kattappana Municipality', 'Kattippara', 'Kattoor', 'Kavalam', 'Kavalangad', 'Kavanur', 'Kavasserri', 'Kavilumpara', 'Kaviyoor', 'Kayakkodi', 'Kayamkulam', 'Kayanna', 'Keerampara', 'Keezhallur', 'Keezhariyur', 'Keezhattur', 'Keezhmad', 'Keezhuparamba', 'Kelakam', 'Keralasseri', 'Khammam', 'Khandwa', 'Kharar', 'Khargone', 'Khliehriat', 'Khunti', 'Kidangoor', 'Kizhakkekallada', 'Kizhakoth', 'Kizhekkencheri', 'Kizhuvilam', 'Kochi', 'Kodakara', 'Kodamthuruth', 'Kodassery', 'Kodenchery', 'Kodumbu', 'Kodumon', 'Kodungallur', 'Kodur', 'Koduvally', 'Koduvayur', 'Kokkyar', 'Kokrajhar', 'Kolachery', 'Kolayad', 'Kolkata', 'Kollam', 'Kollam East', 'Kollayil', 'Kollemkode', 'Kondazhy', 'Kondotty', 'Kongad', 'Konnathadi', 'Konni', 'Koodaranhi', 'Koorachundu', 'Kooroppada', 'Koothali', 'Koothattukulam', 'Koothuparamba', 'Koottickal', 'Koottilangadi', 'Koovappady', 'Koppam', 'Koratty', 'Korba', 'Korea', 'Koruthodu', 'Kota', 'Kota City', 'Kota Rural', 'Kothagudem', 'Kothamangalam', 'Kottakkal', 'Kottamkara', 'Kottangal', 'Kottarakkara', 'Kottathara', 'Kottayam', 'Kottayi', 'Kottiyoor', 'Kottnadu', 'Kottoppadam', 'Kottukal', 'Kottur', 'Kottuvally', 'Koyilandy', 'Koyipuram', 'Kozhencherry', 'Kozhikode', 'Kozhinjampara', 'Kozhuvanal', 'Krishnagiri', 'Krishnapuram', 'Kudayathoor', 'Kulakkada', 'Kulanada', 'Kulasekharapuram', 'Kulathoor', 'Kulathupuzha', 'Kulukkallur', 'Kumaly', 'Kumarakom', 'Kumaramangalam', 'Kumarampathur', 'Kumarapuram', 'Kumbalam', 'Kumbalangy', 'Kummil', 'Kumuram Bheem Asifabad', 'Kundara', 'Kunjimanagalam', 'Kunnamangalam', 'Kunnamkulam', 'Kunnamthanam', 'Kunnathoor', 'Kunnathukal', 'Kunnathunad', 'Kunnothuparambu', 'Kunnukara', 'Kunnummel', 'Kuravilangadu', 'Kurichy', 'Kurnool', 'Kurumathoor', 'Kuruva', 'Kuruvattoor', 'Kuthanur', 'Kuthiyathode', 'Kuttampuzha', 'Kuttichal', 'Kuttippuram', 'Kuttiyatoor', 'Kuttor', 'Kuttyadi', 'Kuzhalmannam', 'Kuzhimanna', 'Kuzhuppily', 'Lakhimpur', 'Latur', 'Lekkidi Peroor', 'Lopoke', 'Lucknow', 'Ludhiana', 'M G Kavu', 'MUZHAKKUNNU', 'Maangattidam', 'Madappally', 'Madavoor', 'Madayi', 'Madurai', 'Mahabubabad', 'Mahabubnagar', 'Mahasamund', 'Mahbubnagar', 'Mairang', 'Majitha', 'Majuli', 'Makkaraparamu', 'Mala', 'Malampuzha', 'Malapattam', 'Malappuram', 'Malayalppuzha', 'Malayattoor', 'Malayinkeezhu', 'Mallappally', 'Mallappuzhassery', 'Maloor', 'Mampad', 'Manakkadu', 'Manaloor', 'Manamboor', 'Mananthavadi', 'Mananthavady', 'Manarkadu', 'Manawala', 'Mancherial', 'Mandla', 'Mandsaur', 'Maneed', 'Mangalam', 'Mangalapuram', 'Mangalore', 'Manickal', 'Manimala', 'Maniyur', 'Manjallur', 'Manjapra', 'Manjeri', 'Manjoor', 'Mankada', 'Mankara', 'Mankulam', 'Mannacherry', 'Mannar', 'Mannarkkad', 'Mannnchery', 'Mannur', 'Maradu', 'Marakkara', 'Maranchery', 'Marangattupally', 'Mararikkulam', 'Mararikulam', 'Maravanthuruthu', 'Marayoor', 'Mariang', 'Mariyapuram', 'Marutharoad', 'Maruthonkara', 'Mathilakam', 'Mathur', 'Matool', 'Mattanur', 'Mattathoor', 'Mavelikkara ULB', 'Mavoor', 'Mawkyrwat', 'Mayyanad', 'Mayyil', 'Medak', 'Medchal', 'Medchal Malkajgiri', 'Meenachil', 'Meenadam', 'Meenanagadi', 'Meerut', 'Melarkodu', 'Melattur', 'Melila', 'Meloor', 'Melukavu', 'Mepayyur', 'Meppadi', 'Mezhuveli', 'Midnapore', 'Mira Road', 'Miraj', 'Mohali (SAS Nagar)', 'Mokeri', 'Moodady', 'Mookkannoor', 'Moonnilavu', 'Moopainad', 'Moopainadu', 'Moorkanad', 'Moothedam', 'Morayur', 'Morbi', 'Morena', 'Morigaon', 'Mudakkal', 'Mudakkuzha', 'Muhamma', 'Mukkam', 'Mulakkuzha', 'Mulakulam', 'Mulanthuruthy', 'Mulavukad', 'Mullassery', 'Mullenkolly', 'Mullurkkara', 'Mulugu', 'Mumbai', 'Mundakkayam', 'Munderi', 'Mundoor', 'Mundrothuruthu', 'Mungeli', 'Munnar', 'Munniyur', 'Muriyad', 'Muthalamada', 'Muthuthala', 'Muthuvallur', 'Muttar', 'Muttil', 'Muttom', 'Muzhappilangad', 'Muzzafarpur', 'Mylapara', 'Mylom', 'Mynagappally', 'Mysore', 'Nadapuram', 'Nadathara', 'Naduvannur', 'Naduvil', 'Nagalasserri', 'Nagaon', 'Nagapattinam', 'Nagarkurnool', 'Nagaur', 'Nagercoil', 'Nagpur', 'Nalbari', 'Nalgonda', 'Namakkal', 'Nandurbar', 'Nanminda', 'Nannambra', 'Nannamukku', 'Nanniyode', 'Naranammoozhi', 'Naranganam', 'Narath', 'Narayanpet', 'Naraynpur', 'Narikunni', 'Naripetta', 'Narsinghpur', 'Nashik', 'Nasik City', 'Nathdwara', 'Nattika', 'Navaikulam', 'Navi Mumbai', 'Nayarambalam', 'Nedumbassery', 'Nedumkandom', 'Nedumkunnam', 'Nedumpana', 'Nedumpram', 'Nedumudy', 'Neduvathoor', 'Neelamperoor', 'Neemuch', 'Neendakara', 'Neendoor', 'Nellaya', 'Nelliampathy', 'Nemmara', 'Nenmanikkara', 'Nenmeni', 'New Amritsar', 'New Delhi', 'New mahi', 'Neyyattinkara Cds', 'Nilambur', 'Nilamel', 'Niramaruthur', 'Niranam', 'Nirmal', 'Niwari', 'Nizamabad', 'Njarakka', 'Njeezhoor', 'Nochad', 'Noida', 'Nongpoh', 'Nongstoin', 'Noolpuzha', 'Nooranad', 'North Garo Hills', 'Oachira', 'Okkal', 'Olavanna', 'Omallor', 'Omasseri', 'Onchium', 'Ongallur', 'Oorakam', 'Oorngattiri', 'Orumanyoor', 'Othukungal', 'Ottappalam', 'Ottasekharamangalam', 'Ozhur', 'PAN State', 'PERAVOOR', 'Paatyam', 'Padinjarathra', 'Padiyoor', 'Padyoor', 'Paingottoor', 'Paippadu', 'Paipra', 'Pakur', 'Pala', 'Palakkad ulb', 'Palamel', 'Palghar', 'Pali', 'Pallarimangalam', 'Pallassana', 'Pallickal', 'Pallickathodu', 'Pallikkal', 'Pallippad', 'Pallipuram', 'Pallivasal', 'Pampady', 'Pampakkuda', 'Panachikadu', 'Panaji', 'Pananchery', 'Panangad', 'Panavally - ruchi', 'Panayam', 'Pandalam Municipality', 'Pandalam Thekkekara', 'Pandikkad', 'Panjal', 'Panmana', 'Panna', 'Pannyannur', 'Panoor', 'Pappinisseri', 'Parakkadavu', 'Parapookkara', 'Parappananagadi', 'Parappur', 'Parassala', 'Parathodu', 'Paravoor', 'Parbhani', 'Pariyaram', 'Parli', 'Paruthur', 'Pathanamthitta', 'Pathanapuram', 'Pathankot', 'Pathiyoor', 'Patiala', 'Patna', 'Pattambi', 'Pattanakkad', 'Pattazhi', 'Pattazhi North', 'Pattencherry', 'Pattithara', 'Pattuvam', 'Pavaratty', 'Pavithreswaram', 'Payyanur', 'Payyavoor', 'Payyoli', 'Pazhayakunnumel', 'Pazhayannur', 'Peddapalli', 'Peddapally', 'Peermade', 'Peralassery', 'Perambalur', 'Perambra', 'Perayam', 'Perinad', 'Peringara', 'Peringom Vayakkara', 'Peringottukkurrissi', 'Perinjanam', 'Perinthalmanna', 'Perumanna', 'Perumanna Klari', 'Perumatti', 'Perumbalam', 'Perumbavoor', 'Perumkadavila', 'Perumpadappu', 'Perunad', 'Peruvallur', 'Peruvayal', 'Peruvemba', 'Pimpri Chinchwad', 'Pinarayi', 'Pindimana', 'Piravam', 'Piravanthoor', 'Pirayiri', 'Polpully', 'Ponmala', 'Ponmudam', 'Ponnani', 'Pookkottukavu', 'Pookkottur', 'Poomangalam', 'Poonjar', 'Poonjar Thekkekkara', 'Poothadi', 'Poothakkulam', 'Pootrikka', 'Poovar', 'Pooyappally', 'Porkulam', 'Port Blair', 'Porur', 'Poruvazhy', 'Pothanikkad', 'Pothencode', 'Pothukal', 'Pozhuthana', 'Pramadam', 'Pratapgarh', 'Puducherry', 'Pudukkad', 'Pudukottai', 'Pulamanthole', 'Pulikkal', 'Pulimath', 'Pulincunnu', 'Pulpatta', 'Punalur', 'Pune', 'Punnappara North', 'Punnapra South', 'Punnayoor', 'Punnayoorkulam', 'Puramattom', 'Purameri', 'Purappuzha', 'Purathur', 'Puthanvelikkara', 'Puthenchira', 'Puthukodu', 'Puthunagaram', 'Puthupally', 'Puthupariyaram', 'Puthuppadi', 'Puthur', 'Puthusseri', 'Puzhakkattiri', 'Raigarh', 'Raipur', 'Raisen', 'Rajakkadu', 'Rajakumari', 'Rajanna Sircilla', 'Rajanna Siricilla', 'Rajasansi', 'Rajgarh', 'Rajkot', 'Rajnandgaon', 'Rajsamand', 'Ramamangalam', 'Ramanathapuram', 'Ramanattukara', 'Ramankary', 'Ramanthalli', 'Ramapuram', 'Ranchi', 'Ranga Reddy', 'Ranga reddy', 'Rangareddy', 'Ranipet', 'Ranni', 'Ranni Angadi', 'Ranni Pazhavangadi', 'Ratlam', 'Rayamangalam', 'Rayya', 'Rewa', 'Rishikesh', 'Rohtak', 'S N Puram', 'Sadiya', 'Sagar', 'Sahibganj', 'Saifai', 'Salem', 'Sangareddy', 'Sangli', 'Santhenpara', 'Sasthamcotta', 'Satna', 'Sawai Madhopur', 'Secunderabad', 'Seethathode', 'Sehore', 'Senapathy', 'Seoni', 'Shahdol', 'Shajapur', 'Sheopur', 'Shillong', 'Shimla', 'Shimoga', 'Shivpuri', 'Sholaur', 'Sholayur', 'Shoranur', 'Siddipet', 'Sidhi', 'Sikar', 'Silchar', 'Siliguri', 'Singrauli', 'Sirohi', 'Sivaganga', 'Sivasagar', 'Solapur', 'Sonepat', 'Sonitpur', 'Sooranadu North', 'Sooranadu South', 'South Garo Hills', 'South Salmara', 'South West Garo Hills', 'Sreekandapuram', 'Sreekrishnapuram', 'Sreemoola nagaram', 'Sri Ganganagar', 'Sriganganagar', 'Srinagar', 'Sukma', 'Surajpur', 'Surat', 'Suryapet', 'T.V. Puram', 'THRIPUNITHURA', 'Tanur', 'Tavanur', 'Tenkasi', 'Tezpur', 'Thachampara', 'Thachanattukara', 'Thakazhi', 'Thalakkad', 'Thalakkulathur', 'Thalanadu', 'Thalappalam', 'Thalassery', 'Thalavady', 'Thalavoor', 'Thalayazham', 'Thalayolaparambu', 'Thaliparamba', 'Thamarakkulam', 'Thamarassery', 'Thanalur', 'Thane', 'Thanjavur', 'Thanneermukkom', 'Thanniam', 'Thannithode', 'Thariode', 'Tharur', 'Thavinjal', 'Thazhakkara', 'Thazhava', 'Thazhekode', 'The Nilgiris', 'Theekoy', 'Thekkekkara', 'Thekkumbhagom', 'Thekkumkara', 'Thenhipalam', 'Theni', 'Thenkara', 'Thenkkurrussi', 'Thenmala', 'Thevalakkara', 'Thidanadu', 'Thikkodi', 'Thillenkeri', 'Thirumarady', 'Thirumittakode', 'Thirunelly', 'Thirupuram', 'Thiruvali', 'Thiruvalla East', 'Thiruvalla West', 'Thiruvallur', 'Thiruvambady', 'Thiruvananthapuram', 'Thiruvaniyoor', 'Thiruvankulam', 'Thiruvarppu', 'Thiruvarur', 'Thiruvegappura', 'Thiruvilwamala', 'Thodiyoor', 'Thodupuzha municipality', 'Thollur', 'Thondernadu', 'Thoothukudi', 'Thottappuzhassery', 'Thrikkadeeri', 'Thrikkakara East', 'Thrikkakara West', 'Thrikkalangode', 'Thrikkaruva', 'Thrikkodithanam', 'Thrikkovilvattom', 'Thrikkunnapuzha', 'Thrikoor', 'Thriprangode', 'Thrissur', 'Thriunavaya', 'Thumpamon', 'Thuravoor', 'Thuravur', 'Thurayur', 'Thuvvur', 'Thycattussery', 'Tikamgarh', 'Tinsukia', 'Tiruchirappalli', 'Tirunelveli', 'Tirupati', 'Tirupattur', 'Tiruppur', 'Tirur', 'Tirurangadi', 'Tiruvallur', 'Tiruvannamalai', 'Tiruvarur', 'Tonk', 'Trichy', 'Triprangottur', 'Trithala', 'Tumkur', 'Tuneri', 'Tura', 'Udaipur', 'Udalguri', 'Udayagiri', 'Udayanapuram', 'Udgir', 'Udhampur', 'Udhayamperoor', 'Udupi', 'Ujjain', 'Ulikkal', 'Ulliyeri', 'Umaria', 'Ummannur', 'Unnnikulam', 'Upputhara', 'Uzhamalaykkal', 'Uzhavoor', 'Vadakara', 'Vadakarapathy', 'Vadakkekkad', 'Vadakkekkara', 'Vadakkenchery', 'Vadanappilly', 'Vadasserikara', 'Vadavannur', 'Vadavukode Puthancruz', 'Vadodara', 'Vaikom', 'Vakathanam', 'Vakkom', 'Valakom', 'Valanchery', 'Valapattanam', 'Valappad', 'Valavannur', 'Valayam', 'Vallachira', 'Vallapuzha', 'Vallatholenagar', 'Vallickode', 'Vallikunnam', 'Vallikunnu', 'Vandanmedu', 'Vandazhi', 'Vandiperiyar', 'Vanimel', 'Vaniyamkulam', 'Vannapuram', 'Varanasi', 'Varantharappilly', 'Varapuzha', 'Varavoor', 'Varkkala', 'Vathikudy', 'Vattamkulam', 'Vattavada', 'Vayalar', 'Vazhakkad', 'Vazhakulam', 'Vazhappally', 'Vazhathope', 'Vazhayur', 'Vazhikkadavu', 'Vazhoor', 'Vechoochira', 'Vechoor', 'Veeyapuram', 'Velinallur', 'Veliyam', 'Veliyamcode', 'Veliyanad', 'Veliyannoor', 'Vellamunda', 'Vellanad', 'Vellangallur', 'Vellarada', 'Vellathooval', 'Vellavoor', 'Vellinezhi', 'Velliyamattam', 'Velloor', 'Vellore', 'Velom', 'Velookkara', 'Veloor', 'Vengad', 'Venganoor', 'Vengapally', 'Vengara', 'Vengola', 'Vengoor', 'Venkitangu', 'Venmony', 'Verka', 'Vettathur', 'Vettikkavala', 'Vettom', 'Vettor', 'Vidisha', 'Vijayapuram', 'Vijayawada', 'Vikarabad', 'Vilakkudy', 'Vilappil', 'Vilayur', 'Villupuram', 'Villyappalli', 'Virudhunagar', 'Visakhapatnam', 'Vithura', 'Vythiri', 'Wadakkanchery', 'Wanaparthy', 'Wandoor', 'Warangal', 'Warangal Rural', 'Warangal Urban', 'Warangal Urban & Rural', 'Wardha', 'Wayanad', 'West Garo Hills', 'West Kallada', 'West Singhbhum', 'Williamnagar', 'Yadadri Bhongiri', 'Yadadri Bhuvanagiri', 'chalavara', 'irinjalakuda block panchayath', 'jashpur nagar', 'kalpetta', 'kothamangalam', 'kunnathunadu', 'nallepilly', 'ottapalam', 'panamaram', 'pandanad', 'pariyaram', 'payam', 'puliyoor', 'pulpally', 'purakkad', 'shoranur', 'thiruvanvandoor']

    districts = ['Unassigned', 'Nicobars', 'North and Middle Andaman', 'South Andaman', 'Unknown', 'Foreign Evacuees', 'Anantapur', 'Chittoor', 'East Godavari', 'Guntur', 'Krishna', 'Kurnool', 'Other State', 'Prakasam', 'S.P.S. Nellore', 'Srikakulam', 'Visakhapatnam', 'Vizianagaram', 'West Godavari', 'Y.S.R. Kadapa', 'Anjaw', 'Changlang', 'East Kameng', 'East Siang', 'Kamle', 'Kra Daadi', 'Kurung Kumey', 'Lepa Rada', 'Lohit', 'Longding', 'Lower Dibang Valley', 'Lower Siang', 'Lower Subansiri', 'Namsai', 'Pakke Kessang', 'Papum Pare', 'Shi Yomi', 'Siang', 'Tawang', 'Tirap', 'Upper Dibang Valley', 'Upper Siang', 'Upper Subansiri', 'West Kameng', 'West Siang', 'Airport Quarantine', 'Baksa', 'Barpeta', 'Biswanath', 'Bongaigaon', 'Cachar', 'Charaideo', 'Chirang', 'Darrang', 'Dhemaji', 'Dhubri', 'Dibrugarh', 'Dima Hasao', 'Goalpara', 'Golaghat', 'Hailakandi', 'Hojai', 'Jorhat', 'Kamrup', 'Kamrup Metropolitan', 'Karbi Anglong', 'Karimganj', 'Kokrajhar', 'Lakhimpur', 'Majuli', 'Morigaon', 'Nagaon', 'Nalbari', 'Other State', 'Sivasagar', 'Sonitpur', 'South Salmara Mankachar', 'Tinsukia', 'Udalguri', 'West Karbi Anglong', 'Unknown', 'Araria', 'Arwal', 'Aurangabad', 'Banka', 'Begusarai', 'Bhagalpur', 'Bhojpur', 'Buxar', 'Darbhanga', 'East Champaran', 'Gaya', 'Gopalganj', 'Jamui', 'Jehanabad', 'Kaimur', 'Katihar', 'Khagaria', 'Kishanganj', 'Lakhisarai', 'Madhepura', 'Madhubani', 'Munger', 'Muzaffarpur', 'Nalanda', 'Nawada', 'Patna', 'Purnia', 'Rohtas', 'Saharsa', 'Samastipur', 'Saran', 'Sheikhpura', 'Sheohar', 'Sitamarhi', 'Siwan', 'Supaul', 'Vaishali', 'West Champaran', 'Chandigarh', 'Other State', 'Balod', 'Baloda Bazar', 'Balrampur', 'Bametara', 'Bastar', 'Bijapur', 'Bilaspur', 'Dakshin Bastar Dantewada', 'Dhamtari', 'Durg', 'Gariaband', 'Janjgir Champa', 'Jashpur', 'Kabeerdham', 'Kondagaon', 'Korba', 'Koriya', 'Mahasamund', 'Mungeli', 'Narayanpur', 'Raigarh', 'Raipur', 'Rajnandgaon', 'Sukma', 'Surajpur', 'Surguja', 'Uttar Bastar Kanker', 'Gaurela Pendra Marwahi', 'Central Delhi', 'East Delhi', 'New Delhi', 'North Delhi', 'North East Delhi', 'North West Delhi', 'Shahdara', 'South Delhi', 'South East Delhi', 'South West Delhi', 'West Delhi', 'Unknown', 'Other State', 'Dadra and Nagar Haveli', 'Daman', 'Diu', 'Other State', 'North Goa', 'South Goa', 'Unknown', 'Other State', 'Ahmedabad', 'Amreli', 'Anand', 'Aravalli', 'Banaskantha', 'Bharuch', 'Bhavnagar', 'Botad', 'Chhota Udaipur', 'Dahod', 'Dang', 'Devbhumi Dwarka', 'Gandhinagar', 'Gir Somnath', 'Jamnagar', 'Junagadh', 'Kheda', 'Kutch', 'Mahisagar', 'Mehsana', 'Morbi', 'Narmada', 'Navsari', 'Panchmahal', 'Patan', 'Porbandar', 'Rajkot', 'Sabarkantha', 'Surat', 'Surendranagar', 'Tapi', 'Vadodara', 'Valsad', 'Bilaspur', 'Chamba', 'Hamirpur', 'Kangra', 'Kinnaur', 'Kullu', 'Lahaul and Spiti', 'Mandi', 'Shimla', 'Sirmaur', 'Solan', 'Una', 'Foreign Evacuees', 'Ambala', 'Bhiwani', 'Charkhi Dadri', 'Faridabad', 'Fatehabad', 'Gurugram', 'Hisar', 'Italians', 'Jhajjar', 'Jind', 'Kaithal', 'Karnal', 'Kurukshetra', 'Mahendragarh', 'Nuh', 'Palwal', 'Panchkula', 'Panipat', 'Rewari', 'Rohtak', 'Sirsa', 'Sonipat', 'Yamunanagar', 'Bokaro', 'Chatra', 'Deoghar', 'Dhanbad', 'Dumka', 'East Singhbhum', 'Garhwa', 'Giridih', 'Godda', 'Gumla', 'Hazaribagh', 'Jamtara', 'Khunti', 'Koderma', 'Latehar', 'Lohardaga', 'Pakur', 'Palamu', 'Ramgarh', 'Ranchi', 'Sahibganj', 'Saraikela-Kharsawan', 'Simdega', 'West Singhbhum', 'Anantnag', 'Bandipora', 'Baramulla', 'Budgam', 'Doda', 'Ganderbal', 'Jammu', 'Kathua', 'Kishtwar', 'Kulgam', 'Kupwara', 'Mirpur', 'Muzaffarabad', 'Pulwama', 'Punch', 'Rajouri', 'Ramban', 'Reasi', 'Samba', 'Shopiyan', 'Srinagar', 'Udhampur', 'Bagalkote', 'Ballari', 'Belagavi', 'Bengaluru Rural', 'Bengaluru Urban', 'Bidar', 'Chamarajanagara', 'Chikkaballapura', 'Chikkamagaluru', 'Chitradurga', 'Dakshina Kannada', 'Davanagere', 'Dharwad', 'Gadag', 'Hassan', 'Haveri', 'Kalaburagi', 'Kodagu', 'Kolar', 'Koppal', 'Mandya', 'Mysuru', 'Other State', 'Raichur', 'Ramanagara', 'Shivamogga', 'Tumakuru', 'Udupi', 'Uttara Kannada', 'Vijayapura', 'Yadgir', 'Other State', 'Alappuzha', 'Ernakulam', 'Idukki', 'Kannur', 'Kasaragod', 'Kollam', 'Kottayam', 'Kozhikode', 'Malappuram', 'Palakkad', 'Pathanamthitta', 'Thiruvananthapuram', 'Thrissur', 'Wayanad', 'Lakshadweep', 'Ahmednagar', 'Akola', 'Amravati', 'Aurangabad', 'Beed', 'Bhandara', 'Buldhana', 'Chandrapur', 'Dhule', 'Gadchiroli', 'Gondia', 'Hingoli', 'Jalgaon', 'Jalna', 'Kolhapur', 'Latur', 'Mumbai', 'Mumbai Suburban', 'Nagpur', 'Nanded', 'Nandurbar', 'Nashik', 'Osmanabad', 'Other State', 'Palghar', 'Parbhani', 'Pune', 'Raigad', 'Ratnagiri', 'Sangli', 'Satara', 'Sindhudurg', 'Solapur', 'Thane', 'Wardha', 'Washim', 'Yavatmal', 'East Garo Hills', 'East Jaintia Hills', 'East Khasi Hills', 'North Garo Hills', 'Ribhoi', 'South Garo Hills', 'South West Garo Hills', 'South West Khasi Hills', 'West Garo Hills', 'West Jaintia Hills', 'West Khasi Hills', 'Unknown', 'Bishnupur', 'Chandel', 'Churachandpur', 'Imphal East', 'Imphal West', 'Jiribam', 'Kakching', 'Kamjong', 'Kangpokpi', 'Noney', 'Pherzawl', 'Senapati', 'Tamenglong', 'Tengnoupal', 'Thoubal', 'Ukhrul', 'Unknown', 'Agar Malwa', 'Alirajpur', 'Anuppur', 'Ashoknagar', 'Balaghat', 'Barwani', 'Betul', 'Bhind', 'Bhopal', 'Burhanpur', 'Chhatarpur', 'Chhindwara', 'Damoh', 'Datia', 'Dewas', 'Dhar', 'Dindori', 'Guna', 'Gwalior', 'Harda', 'Hoshangabad', 'Indore', 'Jabalpur', 'Jhabua', 'Katni', 'Khandwa', 'Khargone', 'Mandla', 'Mandsaur', 'Morena', 'Narsinghpur', 'Neemuch', 'Niwari', 'Other Region', 'Panna', 'Raisen', 'Rajgarh', 'Ratlam', 'Rewa', 'Sagar', 'Satna', 'Sehore', 'Seoni', 'Shahdol', 'Shajapur', 'Sheopur', 'Shivpuri', 'Sidhi', 'Singrauli', 'Tikamgarh', 'Ujjain', 'Umaria', 'Vidisha', 'Aizawl', 'Champhai', 'Hnahthial', 'Khawzawl', 'Kolasib', 'Lawngtlai', 'Lunglei', 'Mamit', 'Saiha', 'Saitual', 'Serchhip', 'Others', 'Dimapur', 'Kiphire', 'Kohima', 'Longleng', 'Mokokchung', 'Mon', 'Peren', 'Phek', 'Tuensang', 'Wokha', 'Zunheboto', 'Unknown', 'Others', 'Angul', 'Balangir', 'Balasore', 'Bargarh', 'Bhadrak', 'Boudh', 'Cuttack', 'Deogarh', 'Dhenkanal', 'Gajapati', 'Ganjam', 'Jagatsinghpur', 'Jajpur', 'Jharsuguda', 'Kalahandi', 'Kandhamal', 'Kendrapara', 'Kendujhar', 'Khordha', 'Koraput', 'Malkangiri', 'Mayurbhanj', 'Nabarangapur', 'Nayagarh', 'Nuapada', 'Puri', 'Rayagada', 'Sambalpur', 'Subarnapur', 'Sundargarh', 'Amritsar', 'Barnala', 'Bathinda', 'Faridkot', 'Fatehgarh Sahib', 'Fazilka', 'Ferozepur', 'Gurdaspur', 'Hoshiarpur', 'Jalandhar', 'Kapurthala', 'Ludhiana', 'Mansa', 'Moga', 'Pathankot', 'Patiala', 'Rupnagar', 'S.A.S. Nagar', 'Sangrur', 'Shahid Bhagat Singh Nagar', 'Sri Muktsar Sahib', 'Tarn Taran', 'Karaikal', 'Mahe', 'Puducherry', 'Yanam', 'Ajmer', 'Alwar', 'Banswara', 'Baran', 'Barmer', 'Bharatpur', 'Bhilwara', 'Bikaner', 'BSF Camp', 'Bundi', 'Chittorgarh', 'Churu', 'Dausa', 'Dholpur', 'Dungarpur', 'Evacuees', 'Ganganagar', 'Hanumangarh', 'Italians', 'Jaipur', 'Jaisalmer', 'Jalore', 'Jhalawar', 'Jhunjhunu', 'Jodhpur', 'Karauli', 'Kota', 'Nagaur', 'Other State', 'Pali', 'Pratapgarh', 'Rajsamand', 'Sawai Madhopur', 'Sikar', 'Sirohi', 'Tonk', 'Udaipur', 'East Sikkim', 'North Sikkim', 'South Sikkim', 'West Sikkim', 'Unknown', 'Foreign Evacuees', 'Other State', 'Adilabad', 'Bhadradri Kothagudem', 'Hyderabad', 'Jagtial', 'Jangaon', 'Jayashankar Bhupalapally', 'Jogulamba Gadwal', 'Kamareddy', 'Karimnagar', 'Khammam', 'Komaram Bheem', 'Mahabubabad', 'Mahabubnagar', 'Mancherial', 'Medak', 'Medchal Malkajgiri', 'Mulugu', 'Nagarkurnool', 'Nalgonda', 'Narayanpet', 'Nirmal', 'Nizamabad', 'Peddapalli', 'Rajanna Sircilla', 'Ranga Reddy', 'Sangareddy', 'Siddipet', 'Suryapet', 'Vikarabad', 'Wanaparthy', 'Warangal Rural', 'Warangal Urban', 'Yadadri Bhuvanagiri', 'Unknown', 'Railway Quarantine', 'Airport Quarantine', 'Other State', 'Ariyalur', 'Chengalpattu', 'Chennai', 'Coimbatore', 'Cuddalore', 'Dharmapuri', 'Dindigul', 'Erode', 'Kallakurichi', 'Kancheepuram', 'Kanyakumari', 'Karur', 'Krishnagiri', 'Madurai', 'Nagapattinam', 'Namakkal', 'Nilgiris', 'Perambalur', 'Pudukkottai', 'Ramanathapuram', 'Ranipet', 'Salem', 'Sivaganga', 'Tenkasi', 'Thanjavur', 'Theni', 'Thiruvallur', 'Thiruvarur', 'Thoothukkudi', 'Tiruchirappalli', 'Tirunelveli', 'Tirupathur', 'Tiruppur', 'Tiruvannamalai', 'Vellore', 'Viluppuram', 'Virudhunagar', 'Dhalai', 'Gomati', 'Khowai', 'North Tripura', 'Sipahijala', 'South Tripura', 'Unokoti', 'West Tripura', 'Unknown', 'Agra', 'Aligarh', 'Ambedkar Nagar', 'Amethi', 'Amroha', 'Auraiya', 'Ayodhya', 'Azamgarh', 'Baghpat', 'Bahraich', 'Ballia', 'Balrampur', 'Banda', 'Barabanki', 'Bareilly', 'Basti', 'Bhadohi', 'Bijnor', 'Budaun', 'Bulandshahr', 'Chandauli', 'Chitrakoot', 'Deoria', 'Etah', 'Etawah', 'Farrukhabad', 'Fatehpur', 'Firozabad', 'Gautam Buddha Nagar', 'Ghaziabad', 'Ghazipur', 'Gonda', 'Gorakhpur', 'Hamirpur', 'Hapur', 'Hardoi', 'Hathras', 'Jalaun', 'Jaunpur', 'Jhansi', 'Kannauj', 'Kanpur Dehat', 'Kanpur Nagar', 'Kasganj', 'Kaushambi', 'Kushinagar', 'Lakhimpur Kheri', 'Lalitpur', 'Lucknow', 'Maharajganj', 'Mahoba', 'Mainpuri', 'Mathura', 'Mau', 'Meerut', 'Mirzapur', 'Moradabad', 'Muzaffarnagar', 'Pilibhit', 'Pratapgarh', 'Prayagraj', 'Rae Bareli', 'Rampur', 'Saharanpur', 'Sambhal', 'Sant Kabir Nagar', 'Shahjahanpur', 'Shamli', 'Shrawasti', 'Siddharthnagar', 'Sitapur', 'Sonbhadra', 'Sultanpur', 'Unnao', 'Varanasi', 'Almora', 'Bageshwar', 'Chamoli', 'Champawat', 'Dehradun', 'Haridwar', 'Nainital', 'Pauri Garhwal', 'Pithoragarh', 'Rudraprayag', 'Tehri Garhwal', 'Udham Singh Nagar', 'Uttarkashi', 'Alipurduar', 'Bankura', 'Birbhum', 'Cooch Behar', 'Dakshin Dinajpur', 'Darjeeling', 'Hooghly', 'Howrah', 'Jalpaiguri', 'Jhargram', 'Kalimpong', 'Kolkata', 'Malda', 'Murshidabad', 'Nadia', 'North 24 Parganas', 'Other State', 'Paschim Bardhaman', 'Paschim Medinipur', 'Purba Bardhaman', 'Purba Medinipur', 'Purulia', 'South 24 Parganas', 'Uttar Dinajpur']


    states_lower = [state.lower().replace(" ","") for state in states]
    districts_lower = [district.lower().replace(" ","") for district in districts]

    f = open("stopwords.txt","r")
    text = f.read()
    refined = text.replace("\"","")
    stopwords = refined.split(",")

    string = str(input("Enter a string\n"))
    tokens = tokenizer(string)

    filtered_tokens = [token for token in tokens if token not in stopwords]

    state_mentioned = []
    district_mentioned = []

    combos = copy.deepcopy(filtered_tokens)
    
    for i in range(len(combos)-1):
        combos.append(combos[i]+combos[i+1])
    
    for token in combos:
        for state in states_lower:
            ratio = fuzz.ratio(state,token)
            if ratio >80:
                state_mentioned.append(state)

    for token in combos:
        for district in districts_lower:
            ratio = fuzz.ratio(district,token)
            if ratio >80:
                district_mentioned.append(district)

    
    state_final = []
    district_final = []

    for state in state_mentioned:
        state_final.append(states[states_lower.index(state)])
    
    for district in district_mentioned:
        district_final.append(districts[districts_lower.index(district)])

    msg = ""
    msg+="Ok. Showing stats for "

    if len(state_final)>=1:
        msg+="the state(s)"
    for i in range(len(state_final)-1,-1,-1):
        if i == 0:
            msg+=" "+str(state_final[i])+", "
            break
        msg+=" "+str(state_final[i])+","

    if len(district_final)>=1:
        msg+=" districts(s)"
    else:
        msg+="."
    for i in range(len(district_final)-1,-1,-1):
        if i == 0:
            msg+=" "+str(district_final[i])+". "
            break
        msg+=" "+str(district_final[i])+","

    print(msg)

    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = []

    for x in filtered_tokens:
        lemmatized_tokens.append(lemmatizer.lemmatize(x))

    requests = []

    service_dict = {"cases":"cases", "case":"cases", "count":"cases", "stats":"cases", "confirmed":"cases", "recovered":"cases", "dead":"cases","deseaced":"cases","number":"cases", "zone":"zone","news":"news"}

    for x in lemmatized_tokens:
        for y,z in service_dict.items():
            ratio = fuzz.ratio(x,y)
            if ratio >80:
                requests.append(z)

    requests = list(set(requests))

    stt_case_info_dict = {}
    dis_case_info_dict = {}
    dis_zone_dict = {}



    #State cases
    state_lst,conf_final,rec_final,des_final = get_table()
    combined = pd.concat([state_lst,conf_final,rec_final,des_final],axis=1)
    combined.columns = ["state","conf","rec","des"]


    

    #Zone


    for req in requests:
        for stt in state_final:

            if req == "cases":
                state_data = combined.loc[combined["state"] == stt]

                state_conf = int(state_data["conf"])
                state_recovered = int(state_data["rec"])
                state_des = int(state_data["des"])

                stt_case_info_dict[stt]=[state_conf,state_recovered,state_des]

            


                

        for dis in district_final:

            if req == "cases":

                dinf = districtwise_info_dist(dis)
                disname = list(dinf.keys())[0]
                val = list(dinf.values())[0]
                act,conf,dec,rec = val[0],val[1],val[2],val[3]
                dis_case_info_dict[disname]=[conf,act,rec,dec]
                

            if req == "zone":
                info = zone_info_fun_dis(dis)

                dis_zone_dict[dis]=info["zone"]



    if len(requests)==0:
        print("No option chosen.")


    if str(dis_case_info_dict)!=str("{}"):
        
        for x,y in dis_case_info_dict.items():
            print("For district {} there are {} confirmed cases, {} active cases, {} recoveries and {} deaths.".format(x,y[0],y[1],y[2],y[3]))

    if str(stt_case_info_dict)!=str("{}"):
        
        for x,y in stt_case_info_dict.items():
            print("For state {} there are {} confirmed cases, {} recoveries and {} deaths.".format(x,y[0],y[1],y[2]))

    if str(dis_zone_dict)!=str("{}"):

        for x, y in  dis_zone_dict.items():

            print("{} is in {} zone.".format(x,y))


if __name__=="__main__":
    while 1:
        chat()