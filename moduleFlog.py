# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 12:20:00 2017

@author: ivan
"""

import mysql.connector
from lxml import etree
import ConfigParser
import os.path as op


def setConexion(db_user,db_password,db_host,db_database):
    cnx=mysql.connector.connect(user=db_user,password=db_password,host=db_host,database=db_database)
    return cnx

def mapBlogs(blog):
    if blog=="bcommebon":
        return "cuisine1"
    if blog=="beaualalouche":
        return "cuisine2"
    if blog=="coupleofpixels":
        return "jeuxvideo1"
    if blog=="domadoo":
        return "technologie1"
    if blog=="domotique34":
        return "technologie5"
    if blog=="francoischarlet":
        return "droit1"
    if blog=="johncouscous":
        return "jeuxvideo2"
    if blog=="josdblog":
        return "technologie2"
    if blog=="journaldugamer":
        return "jeuxvideo3"
    if blog=="julsa":
        return "jeuxvideo4"
    if blog=="jurilexblog":
        return "droit2"
    if blog=="lagourmandiseselonangie":
        return "cuisine3"
    if blog=="maisonetdomotique":
        return "technologie3"
    if blog=="paralipomenes":
        return "droit3"
    if blog=="pechedegourmand":
        return "cuisine4"
    if blog=="philippebilger":
        return "droit4"
    if blog=="prendreuncafe":
        return "technologie4"
    if blog=="roxarmy":
        return "jeuxvideo5"
    if blog=="shots":
        return "technologie6"
    if blog=="toutchilink":
        return "jeuxvideo6"
    return blog    

class Post:
    date=""
    author=""
    tags=[]
    cats=[]
    text=""
    title=""
    locfile=""
    dbID=0

    def __init__(self,myfile,dbRel=0):
        f=open(myfile)
        document = etree.fromstring(f.read())
        
        self.date=document.xpath("date/text()")
    #    print date[0]
        
        self.title=document.xpath("title/text()")
    #    print title[0]    
        
        self.author=document.xpath("author/text()")
    #   print author[0]
        
        self.tags=document.xpath("tags_set/tag/text()")
    #    for tag in tags:
    #        print tag.text
        
        self.cats=document.xpath("categories_set/category/text()")
    #    for cat in cats:
    #       print cat.text
            
        self.text=document.xpath("text/text()")[0]
    #    print text
        self.locfile=myfile
        self.dbID=dbRel
        f.close
        
    def __len__(self):
        return len(self.text)


class microCorpus:
    
    mcCorpus=[]
    
    def __init__(self,filist):
        self.mcCorpus=[]
        for elem in filist:
            if op.isfile(elem[0]):
                x=Post(elem[0],elem[1])
                self.mcCorpus.append(x)
            
    def getInstancesTexts(self):
        inst=[]
        for x in self.mcCorpus:
            inst.append(x.text)
        return inst
        
    def getInstancesIds(self):
        inst=[]
        for x in self.mcCorpus:
            inst.append(x.dbID)
        return inst
    
    def getInstancesTextsCategories(self):
        inst=[]
        for x in self.mcCorpus:
            inst.append([x.text,x.cats])
        return inst
        
    def getInstancesCategories(self):
        inst=[]
        for x in self.mcCorpus:
            inst.append(set(x.cats))
        return inst
        
    def getInstancesTextsCategoriesFiltered(self,filterLbls):
        inst=[]
        for x in self.mcCorpus:
            catg=[]
            for z in x.cats:
                if z in filterLbls:
                    catg.append(z)
            inst.append(set(catg))
        return inst


class Blog:
    "Blog handling class"
    name=""
    idC=""
    catgs=[]
    keys=[]
    dbCon=0
    loc=""
    db_user=""
    db_password=""
    db_host=""
    db_database=""
    
    def __init__(self,nam):
        config=ConfigParser.RawConfigParser()
        config.read('flog.conf')
        self.db_user=config.get('DataBase', 'user')
        self.db_password=config.get('DataBase', 'password')
        self.db_host=config.get('DataBase', 'host')
        self.db_database=config.get('DataBase', 'database')
        corpus_loc=config.get('Corpus', 'corpus_dir')        
        cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
        dbH=cnx.cursor()        
        
        if corpus_loc[-1:]!='/':
            corpus_loc+="/x"
        else:
            corpus_loc+="x"

        dbH.execute("SELECT idblog, blogName FROM blog where blogName='"+nam+"';")
        bx=dbH.fetchone()
        self.name=bx[1]
        self.idC=bx[0]
        self.loc=corpus_loc+nam+"/"
        dbH.execute("SELECT idcategory FROM category where blog="+str(self.idC)+";")
        for ct in dbH:
            self.catgs.append(ct[0])
        dbH.execute("SELECT idtag FROM tag where blog="+str(self.idC)+";")
        for tg in dbH:
            self.keys.append(tg[0])
        dbH.close()
            
    def getAllPostsFiles(self):
        cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
        self.dbCon=cnx.cursor()
        postF=[]
        sep=""
        if self.loc[-1:]!='/':
            sep="/"
        self.dbCon.execute("select post.file from post where blog="+str(self.idC))
        for pst in self.dbCon:
            postF.append(self.loc+sep+pst[0])
        self.dbCon.close()
        return postF
        
    def getAllCategoriesNames(self):
        cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
        self.dbCon=cnx.cursor()
        cats=""
        catNam=[]
        for cat in self.catgs:
            cats+=str(cat)+","
        self.dbCon.execute("SELECT categoryName FROM category where idcategory in ("+cats[:-1]+");")
        for cN in self.dbCon:
            catNam.append(cN[0])
        self.dbCon.close()
        return catNam
        
    def getAllCategoriesFreq(self):
        cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
        self.dbCon=cnx.cursor()
        cats=""
        catNam=[]
        for cat in self.catgs:
            cats+=str(cat)+","
        self.dbCon.execute("select category.categoryName, count(*) as freq, category.idcategory as catg from category_link inner join category on category_link.cat=category.idcategory where category.blog="+str(self.idC)+" group by category_link.cat order by freq desc, categoryName asc;")
        for cN in self.dbCon:
            catNam.append(cN)
        self.dbCon.close()
        return catNam
        
    def setLocation(self,locdir):
        self.loc=locdir
        
    def getACategoryName(self,idcat):
        if idcat in self.catgs:
            cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
            self.dbCon=cnx.cursor()
            self.dbCon.execute("SELECT categoryName FROM category where idcategory="+str(idcat)+";")
            name=self.dbCon.fetchone()[0]
            self.dbCon.close()
            return name
        else:
            return "Category not found"

    def getPostsFromAYear(self,year):
        catDoc=[]
        sep=""
        if self.loc[-1:]!='/':
            sep="/"
        cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
        self.dbCon=cnx.cursor()
        self.dbCon.execute("select post.file, post.idBlogEntry from post where post.blog="+str(self.idC)+" and YEAR(post.date)='"+str(year)+"';")
        for fl in self.dbCon:
            catDoc.append([self.loc+sep+fl[0],fl[1]])
        self.dbCon.close()
        return catDoc
        
    def getPostsBetweeDates(self,datea,dateb):
        catDoc=[]
        sep=""
        if datea>dateb:
            datetmp=dateb
            dateb=datea
            datea=datetmp
        if self.loc[-1:]!='/':
            sep="/"
        cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
        self.dbCon=cnx.cursor()
        self.dbCon.execute("select post.file, post.idBlogEntry from post where post.blog="+str(self.idC)+" and post.date>='"+str(datea)+"' and post.date<='"+str(dateb)+"';")
        for fl in self.dbCon:
            catDoc.append([self.loc+sep+fl[0],fl[1]])
        self.dbCon.close()
        return catDoc

    def getPostsFromACategory(self,idcat):
        catDoc=[]
        sep=""
        if self.loc[-1:]!='/':
            sep="/"
        if idcat in self.catgs:
            cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
            self.dbCon=cnx.cursor()
            self.dbCon.execute("select post.file, entry from category_link inner join post on category_link.entry=post.idblogEntry where category_link.cat="+str(idcat)+";")
            for fl in self.dbCon:
                catDoc.append([self.loc+sep+fl[0],fl[1]])
            self.dbCon.close()
            return catDoc
        else:
            return "Category not found"
            
    def getIntersectionSizeBetweenCatACatB(self,a,b):
        if a in self.catgs and b in self.catgs:
            cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
            self.dbCon=cnx.cursor()
            self.dbCon.execute("select count(*) as i from category_link where cat="+str(a)+" and entry in (select entry from category_link where cat="+str(b)+");")
            interx=self.dbCon.fetchone()[0]
            self.dbCon.close()
            return int(interx)
        else:
            return "Category not found"
            
    def getBlogOriginDate(self):
        cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
        self.dbCon=cnx.cursor()
        self.dbCon.execute("select min(date) as origin from post where blog="+str(self.idC)+";")
        oDate=self.dbCon.fetchone()[0]
        self.dbCon.close()
        return oDate
        
    def getBlogLastDate(self):
        cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
        self.dbCon=cnx.cursor()
        self.dbCon.execute("select max(date) as origin from post where blog="+str(self.idC)+";")
        lDate=self.dbCon.fetchone()[0]
        self.dbCon.close()
        return lDate
    
    def getNumberOfMonthsTheBlogSBeenActive(self):
        cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
        self.dbCon=cnx.cursor()
        self.dbCon.execute("select TIMESTAMPDIFF(MONTH,min(date),max(date)) as diff from post where blog="+str(self.idC)+";")
        nMonths=self.dbCon.fetchone()[0]
        self.dbCon.close()
        return int(nMonths)+1
        
    def getCategoryFrequenciesPerMonth(self,mode="desc"):
        catFM=[]
        cnx=mysql.connector.connect(user=self.db_user,password=self.db_password,host=self.db_host,database=self.db_database)
        self.dbCon=cnx.cursor()
        self.dbCon.execute("select frecalc.*,tot,freq/tot as norm from (select cat, mesdiff, count(*) as freq from (select cat, mesdiff, concat(cat,'-',mesdiff) as grouper from(select cat,post.date, TIMESTAMPDIFF(MONTH,(select min(date) as origin from post where blog="+str(self.idC)+"), post.date) as mesdiff from category_link inner join post on category_link.entry=post.idblogEntry where blog="+str(self.idC)+" order by date)as catdatemonth) as groupingT group by grouper order by cat, mesdiff) as frecalc inner join (select cat, count(*) as tot from category_link inner join category on category_link.cat=category.idcategory where category.blog="+str(self.idC)+" group by cat) as tots on tots.cat=frecalc.cat order by tot "+mode+";")
        for fl in self.dbCon:
            catFM.append(fl)
        self.dbCon.close()
        return catFM
