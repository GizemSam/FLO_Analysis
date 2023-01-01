#!/usr/bin/env python
# coding: utf-8

# In[3]:


import datetime as dt
import pandas as pd
import matplotlib as plt


# In[10]:


pip install Lifetimes


# In[11]:


from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions


# In[71]:


pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
from sklearn.preprocessing import MinMaxScaler


# master_id: Eşsiz müşteri numarası
# order_channel: Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile)
# last_order_channel: En son alışverişin yapıldığı kanal
# first_order_date: Müşterinin yaptığı ilk alışveriş tarihi
# last_order_date: Müşterinin yaptığı son alışveriş tarihi
# last_order_date_online: Müşterinin online platformda yaptığı son alışveriş tarihi
# last_order_date_offline: Müşterinin offline platformda yaptığı son alışveriş tarihi
# order_num_total_ever_online: Müşterinin online platformda yaptığı toplam alışveriş sayısı
# order_num_total_ever_offline: Müşterinin offline'da yaptığı toplam alışveriş sayısı
# customer_value_total_ever_offline: Müşterinin offline alışverişlerinde ödediği toplam ücret
# customer_value_total_ever_online: Müşterinin online alışverişlerinde ödediği toplam ücret
# interested_in_categories_12: Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listei

# Adım 1: flo_data_20K.csv verisini okuyunuz.Dataframe’in kopyasını oluşturunuz

# In[17]:


df_ = pd.read_csv("flo_data_20k.csv")


# In[18]:


df = df_.copy()


# Adım 2: Veri setinde
# a. İlk 10 gözlem,
# b. Değişken isimleri,
# c. Betimsel istatistik,
# d. Boş değer,
# e. Değişken tipleri, incelemesi yapınız.
# 

# In[22]:


df.head(10) #İlk 10 gözlem
df.columns #Değişken isimleri
df.describe() #Betimsel istatistik
df.isnull().sum() #Boş değer
df.info() #Değişken tipleri






# Adım 3: Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir. Her bir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturunuz.

# In[38]:


df["num_total"]=df["order_num_total_ever_online"]+df["order_num_total_ever_offline"] # toplam alışveriş sayısı
df["value_total"]=df["customer_value_total_ever_offline"]+df["customer_value_total_ever_online"] #toplam harcama
df.head()


# Adım 4: Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.

# In[51]:


df.info()

#Aşağıda değişklik yapmak istediğimiz kolonları seçtik ve pandasdan datatime'a  çevirdik.

df[["first_order_date", "last_order_date", "last_order_date_online","last_order_date_offline"]] =df[["first_order_date",
                                                                                                     "last_order_date",
                                                                                                     "last_order_date_online", 
                                                                                                     "last_order_date_offline"]].apply(pd.to_datetime)

#2. yol aşağıdaki gibi yaparsak içinde "date" geçen colonları "datetime" a çevir yapabiliriz.

#date_columns = df.columns[df.columns.str.contains("date")]
#df[date_columns] = df[date_columns].apply(pd.to_datetime)


# Adım 5: Alışveriş kanallarındaki müşteri sayısının, toplam alınan ürün sayısının ve toplam harcamaların dağılımına bakınız.

# In[52]:


df.groupby("order_channel").agg({"master_id":"count",
                                 "num_total":"sum",
                                 "value_total":"sum"})
#Alışveriş kanallarına göre dağılımlarına bakıyoruz.


# Adım 6: En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.

# In[56]:


df.sort_values("value_total", ascending=False)[:10] #sort_values kullanarak belirtilen kolona göre sıralama yaptık


# Adım 7: En fazla siparişi veren ilk 10 müşteriyi sıralayınız.

# In[57]:


df.sort_values("num_total", ascending=False)[:10]


# Adım 8: Veri ön hazırlık sürecini fonksiyonlaştırınız.

# In[58]:


def preliminary_data(data):
data["num_total"]=data["order_num_total_ever_online"]+data["order_num_total_ever_offline"] # toplam alışveriş sayısı
data["value_total"]=data["customer_value_total_ever_offline"]+data["customer_value_total_ever_online"] #toplam harcama
date_columns = data.columns[data.columns.str.contains("date")]
data[date_columns] = data[date_columns].apply(pd.to_datetime)
return def


    
    
    


 # Görev 2: RFM Metriklerinin Hesaplanması#

# Adım 1: Recency, Frequency ve Monetary tanımlarını yapınız

# In[ ]:


#Recency(yenilik : analizin yapıldığı tarih- müşterinein son satın aldığı tarih)
#Frequency(müşterinin toplan satın alması) 
#Monetary(parasal değer)


# Adım 2: Müşteri özelinde Recency, Frequency ve Monetary metriklerini hesaplayınız.
# -Recency değerini hesaplamak için analiz tarihini maksimum tarihten 2 gün sonrası seçebilirsiniz.
# Adım 3: Hesapladığınız metrikleri rfm isimli bir değişkene atayınız.
# Adım 4: Oluşturduğunuz metriklerin isimlerini recency, frequency ve monetary olarak değiştiriniz.

# In[76]:


import datetime 
# işlemleri daha kolay yapmak için kütüphanemizi import ediyoruz.


# In[81]:


analysis_date= df["last_order_date"].max() + datetime.timedelta(days=2) #2gün sonrası


# In[83]:


analysis_date # yeni oluşturduğumuz analiz tarihini kontrol ediyoruz.


# In[85]:


#-Recency değerini hesaplamak için analiz tarihini maksimum tarihten 2 gün sonrası seçebilirsiniz
rfm = pd.DataFrame()
rfm["customer_id"] = df["master_id"] # işlem yaparken colomnsisimlerini de değiştiriyoruz.
rfm["recency"] = (analysis_date - df["last_order_date"]).astype('timedelta64[D]') #astype('timedelta64[D]') ile gün cinsine çeviriyoruz.
rfm["frequency"] = df["num_total"]
rfm["monetary"] = df["value_total"]
rfm.head()


# #Görev 3: RF Skorunun Hesaplanması

# Adım 1: Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çeviriniz. 
# Adım 2: Bu skorları recency_score, frequency_score ve monetary_score olarak kaydediniz.
# Adım 3: recency_score ve frequency_score’u tek bir değişken olarak ifade ediniz ve RF_SCORE olarak kaydediniz. 

# In[86]:


rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1]) # recency'de küçük olana büyük puan verilir.

rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]) # küçük gördüğüne küçük puan ver.Frequency(müşterinin toplan satın alması) 
#.rank(method="first") kullanmamızın nedeni duplicate kayıtlar olabiliyor hata vermemesi için ilk bulduğu segmenti atıyoruz.
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])#Monetary küçük olana küçük değeri ver(parasal değer)

rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))
rfm.head()


# #Görev 4: RF Skorunun Segment Olarak Tanımlanması

# Adım 1: Oluşturulan RF skorları için segment tanımlamaları yapınız.
# Adım 2: Aşağıdaki seg_map yardımı ile skorları segmentlere çeviriniz

# Adım 2:
# 
#     r'[1-2][1-2]': 'hibernating', #1. elemanda 1 yada 2  görürsen , 2.elamanda 1 yada 2 gçrürsen hibernating' yaz demek
#     r'[1-2][3-4]': 'at_Risk',
#     r'[1-2]5': 'cant_loose',  # 2. elemanda  görürsen köşeli parantez - varsa yada demek.
#     r'3[1-2]': 'about_to_sleep',
#     r'33': 'need_attention',  # 1 elemanında ve 2. elemanında 3 görürsen bu isimldirmeyi yap
#     r'[3-4][4-5]': 'loyal_customers',
#     r'41': 'promising',
#     r'51': 'new_customers',
#     r'[4-5][2-3]': 'potential_loyalists',
#     r'5[4-5]': 'champions'

# In[87]:


seg_map = {
    r'[1-2][1-2]': 'hibernating', 
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',  
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',  
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}


# In[88]:


rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)#RF skorları için segment tanımlamaları


# In[90]:


rfm.head(10)#ilk 10 değere bakalım


# Görev 5: Aksiyon Zamanı
# 

# Adım 1: Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.

# In[91]:


rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean"])


# Adım 2: RFM analizi yardımıyla aşağıda verilen 2 case için ilgili profildeki müşterileri bulun ve müşteri id'lerini csv olarak kaydediniz.

# a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri
# tercihlerinin üstünde. Bu nedenle markanın tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak
# iletişime geçmek isteniliyor. Sadık müşterilerinden(champions, loyal_customers) ve kadın kategorisinden alışveriş
# yapan kişiler özel olarak iletişim kurulacak müşteriler. Bu müşterilerin id numaralarını csv dosyasına kaydediniz

# In[100]:


target_customers = rfm[rfm["segment"].isin(["champions","loyal_customers"])]["customer_id"] # ıd numarasına göre champions","loyal_customers olan müşteri numaralarını getirdik


# In[105]:


cust_ids = df[(df["master_id"].isin(target_customers)) &(df["interested_in_categories_12"].str.contains("KADIN"))]["master_id"]
#müşteri ıd sına göre yukarıdaki filtremizi ve interested_in_categories_12 colonunda içinde "kadın" yazanları müşteri ıdsına göre getir bunları birleştir dedik.


# In[111]:


cust_ids.to_csv("yenii_marka_hedef_müşteri_id.csv", index=True) 
cust_ids.to_csv("yeni_marka_hedef_müşteri_id.csv", index=False)
# dosyamızın konumuna bu isimle csv olarak kaydettik.
#index=True ile index numaralı olarak kaydettik.
#index=False ile de index numarasız olarak kaydettik.


# 
# b. Erkek ve Çocuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen "geçmişte
# iyi müşteri olan ama uzun süredir alışveriş yapmayan" "kaybedilmemesi gereken müşteriler", "uykuda olanlar" ve "yeni
# gelen müşteriler" özel olarak hedef alınmak isteniyor. Uygun profildeki müşterilerin id'lerini csv dosyasına kaydediniz
# 

# In[112]:


target_customers_b = rfm[rfm["segment"].isin(["cant_loose","hibernating","new_customers,at_Risk"])]["customer_id"]
# tırnak içinde belirtilen müşterileri katogerisini id numarsına göre getirdik


# In[118]:


cust_ids_b = df[(df["master_id"].isin(target_customers_b)) &(df["interested_in_categories_12"].str.contains("ERKEK"))|(df["interested_in_categories_12"].str.contains("COCUK"))]["master_id"]
#hedeflediğimiz müşterilere göre erkek ve cocuk katogerisine sahip olanları listeledik


# In[120]:


cust_ids_b.to_csv("indirim_hedef_müşteri_id.csv", index=True) 
cust_ids_b.to_csv("indirimm_hedef_müşteri_id.csv", index=False)
# dosyamızın konumuna bu isimle csv olarak kaydettik.
#index=True ile index numaralı olarak kaydettik.
#index=False ile de index numarasız olarak kaydettik.


# In[ ]:





# In[ ]:




