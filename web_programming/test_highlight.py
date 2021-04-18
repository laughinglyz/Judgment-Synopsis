from elasticsearch import Elasticsearch

es = Elasticsearch(["localhost:3000"])
neutral = "[2009] HKCFI 2104"
index = "hklii_en_case"

body = {
    "query":{
        "match":{
            "neutral":neutral
        }
    }
}

res = es.search(index=index,body=body)
doc_id = 48552
doc = res['hits']['hits'][0]['_source']
print(doc['neutral'])
print(doc_id)
print(doc['content'])

content = """
<body>
 <!--sino hidden DIS 65218 -->
 <form name="search_body">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
   <tr>
    <td>
     <p style="text-align:right">
      HCCC241/2008
     </p>
     <p style="text-align:center">
      IN THE HIGH COURT OF THE
     </p>
     <p style="text-align:center">
      HONG KONG SPECIAL ADMINISTRATIVE REGION
     </p>
     <p style="text-align:center">
      COURT OF FIRST INSTANCE
     </p>
     <p style="text-align:center">
      CRIMINAL CASE NO. 241 OF 2008
     </p>
     <blockquote>
      <p style="text-align:center">
       <b>
        ----------------------
       </b>
      </p>
     </blockquote>
     <!--sino section party -->
     <parties>
      <table border="0" width="100%">
       <tr>
        <td style="text-align:center" width="25%">
        </td>
        <td style="text-align:center" width="50%">
         HKSAR
        </td>
        <td style="text-align:center" width="25%">
        </td>
       </tr>
       <tr>
        <td style="text-align:center">
        </td>
        <td style="text-align:center">
         v.
        </td>
        <td style="text-align:center">
        </td>
       </tr>
       <tr>
        <td style="text-align:center">
        </td>
        <td style="text-align:center">
         Mwaniki, Catherine Waithira
        </td>
        <td style="text-align:center">
        </td>
       </tr>
      </table>
     </parties>
     <!--sino section text -->
     <blockquote>
      <p style="text-align:center">
       <b>
        ----------------------
       </b>
      </p>
     </blockquote>
     <p>
      <b>
      </b>
     </p>
     <!--sino section coram -->
     <coram>
      Before   Deputy High Court Judge Geiser
     </coram>
     <!--sino section text -->
     <br/>
     <date>
      <p>
       Date: 30 March 2009 at 11.52 am
      </p>
     </date>
     <!--sino section representation -->
     <representation>
      <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse" width="100%">
       <tr>
        <td valign="top" width="11%">
         <p>
          Present:
         </p>
        </td>
        <td valign="top" width="89%">
         <p>
          Miss Grace Chan, SPP, of the Department of Justice,for HKSAR
          <br/>
          Mr Frederic C Whitehouse, instructed by Chin &amp; Associates, for the 1st Accused
         </p>
        </td>
       </tr>
      </table>
     </representation>
     <!--sino section text -->
     <!--sino section charge -->
     <charge>
      <p>
       <div class = "important">Offence:  Trafficking in dangerous drugs (販運危險藥物)</div>
      </p>
     </charge>
     <!--sino section text -->
     <p>
      <b>
      </b>
     </p>
     <p style="text-align:center">
      <b>
       <u>
        Transcript of the Audio Recording
        <br/>
        of the Sentence in the above case
       </u>
      </b>
     </p>
     <p>
      <b>
      </b>
     </p>
     <p>
      <div class = "important">COURT:  You, madam, pleaded guilty to an offence of trafficking in dangerous drugs contrary to section 4(1)(a) and (3) of the</div>
      <a href="/en/legis/ord/134/">
       Dangerous Drugs Ordinance
      </a>
      ,
      <a href="/en/legis/ord/134/">
       Cap. 134
      </a>
      , Laws of Hong Kong, the particulars being that, on 8 June of last year, at Chek Lap Kok International Airport, you had in your possession 881.38 grammes of a mixture containing 613.74 grammes of heroin hydrochloride.
     </p>
     <p>
      <div class = "important">The facts which you have agreed indicate that upon your arrival at Hong Kong International Airport, you were searched and a quantity of heroin in the form of pellets were found inside the pants that you were wearing and, subsequently, when you were taken to hospital, a further 65 pellets of heroin were discharged from your body.</div>
     </p>
     <p>
      <div class = "important">You told the police, in a record of interview, that you had been recruited by a person called ‘Mike’ in Mumbai to collect the drugs from Delhi and bring them to Hong Kong. </div> In Delhi, you met another male called ‘Joe’ who gave you the pellets to swallow, which you did, and you then brought them to Hong Kong.  <div class = "important">For this, you were to be paid US$5,000 for successful delivery to Hong Kong.</div>
     </p>
     <p>
      I have read the letter that you have written to me and which has been handed to me by your counsel Mr Whitehouse.  It makes for tragic reading.  <div class = "important">You are 48 years of age now, of clear record, a single mother, having three children of your own. </div> <div class = "important">You also, I understand, have the responsibility of looking after seven other children, four nephews and three nieces. </div> <div class = "important">These are children of your two sisters, both of whom, together with their respective husbands, have now died of Aids.</div>
     </p>
     <p>
      <div class = "important">In addition to this, to add to your overwhelming difficulties, your shop and your home were burnt down during the post-election riots that took place in Kenya at the end of 2007. </div> <div class = "important">As a result of your desperate situation, you say yourself in the letter, you were easy prey to the marauding drug bosses who brought you into their cartel.</div>
     </p>
     <p>
      I am asked by your counsel to take all of these matters into account in sentencing you.  <div class = "important">I will do so and I will also give you credit for your plea of guilty to this offence, which is an indication of your genuine remorse.</div>
     </p>
     <p>
      <div class = "important">I must, however, also bear in mind that there is an aggravating feature here and that is that there is, quite obviously, an international element to this offence in the sense that this large quantity of drugs was brought into Hong Kong by yourself from overseas.</div>
     </p>
     <p>
      The sentencing guidelines contained in
      <u>
       Regina v Lau Tak Ming &amp; Others
      </u>
      (1990)
      <a href="http://www.austlii.edu.au/cgi-bin/LawCite?cit=2 HKLR 370">
       2 HKLR 370
      </a>
      puts you just outside the 15 to 20-year starting point bracket, as you had in your possession over 600 grammes of heroin.  <div class = "important">I am prepared, however, to invoke a starting point that keeps you within that sentencing bracket but, due to the aggravating feature that I have referred to, I find that I am unable to adopt a starting point of less than 20 years’ imprisonment.</div>
     </p>
     <p>
      Indeed, I do adopt that as my starting point.  <div class = "important">I will discount that starting point by one-third to take account of your plea of guilty, coming to 13 years 4 months’ imprisonment.</div>
     </p>
     <p>
      <div class = "important">In addition, and as an act of mercy, I will give you a further discount of 16 months’ imprisonment to take account of the tragic circumstances that you found yourself in, leading you to commit this offence, arriving at a sentence of 12 years’ imprisonment.</div>
     </p>
     <p>
      <b>
      </b>
     </p>
    </td>
   </tr>
  </table>
 </form>
</body>"""

# print((es.update(index=index,id=doc_id, body={"doc": {"content": content}})))

original_content = """
<body>
 <!--sino hidden DIS 65218 -->
 <form name="search_body">
  <table border="0" cellpadding="0" cellspacing="0" width="100%">
   <tr>
    <td>
     <p style="text-align:right">
      HCCC241/2008
     </p>
     <p style="text-align:center">
      IN THE HIGH COURT OF THE
     </p>
     <p style="text-align:center">
      HONG KONG SPECIAL ADMINISTRATIVE REGION
     </p>
     <p style="text-align:center">
      COURT OF FIRST INSTANCE
     </p>
     <p style="text-align:center">
      CRIMINAL CASE NO. 241 OF 2008
     </p>
     <blockquote>
      <p style="text-align:center">
       <b>
        ----------------------
       </b>
      </p>
     </blockquote>
     <!--sino section party -->
     <parties>
      <table border="0" width="100%">
       <tr>
        <td style="text-align:center" width="25%">
        </td>
        <td style="text-align:center" width="50%">
         HKSAR
        </td>
        <td style="text-align:center" width="25%">
        </td>
       </tr>
       <tr>
        <td style="text-align:center">
        </td>
        <td style="text-align:center">
         v.
        </td>
        <td style="text-align:center">
        </td>
       </tr>
       <tr>
        <td style="text-align:center">
        </td>
        <td style="text-align:center">
         Mwaniki, Catherine Waithira
        </td>
        <td style="text-align:center">
        </td>
       </tr>
      </table>
     </parties>
     <!--sino section text -->
     <blockquote>
      <p style="text-align:center">
       <b>
        ----------------------
       </b>
      </p>
     </blockquote>
     <p>
      <b>
      </b>
     </p>
     <!--sino section coram -->
     <coram>
      Before   Deputy High Court Judge Geiser
     </coram>
     <!--sino section text -->
     <br/>
     <date>
      <p>
       Date: 30 March 2009 at 11.52 am
      </p>
     </date>
     <!--sino section representation -->
     <representation>
      <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse" width="100%">
       <tr>
        <td valign="top" width="11%">
         <p>
          Present:
         </p>
        </td>
        <td valign="top" width="89%">
         <p>
          Miss Grace Chan, SPP, of the Department of Justice,for HKSAR
          <br/>
          Mr Frederic C Whitehouse, instructed by Chin &amp; Associates, for the 1st Accused
         </p>
        </td>
       </tr>
      </table>
     </representation>
     <!--sino section text -->
     <!--sino section charge -->
     <charge>
      <p>
       Offence:  Trafficking in dangerous drugs (販運危險藥物)
      </p>
     </charge>
     <!--sino section text -->
     <p>
      <b>
      </b>
     </p>
     <p style="text-align:center">
      <b>
       <u>
        Transcript of the Audio Recording
        <br/>
        of the Sentence in the above case
       </u>
      </b>
     </p>
     <p>
      <b>
      </b>
     </p>
     <p>
      COURT:  You, madam, pleaded guilty to an offence of trafficking in dangerous drugs contrary to section 4(1)(a) and (3) of the
      <a href="/en/legis/ord/134/">
       Dangerous Drugs Ordinance
      </a>
      ,
      <a href="/en/legis/ord/134/">
       Cap. 134
      </a>
      , Laws of Hong Kong, the particulars being that, on 8 June of last year, at Chek Lap Kok International Airport, you had in your possession 881.38 grammes of a mixture containing 613.74 grammes of heroin hydrochloride.
     </p>
     <p>
      The facts which you have agreed indicate that upon your arrival at Hong Kong International Airport, you were searched and a quantity of heroin in the form of pellets were found inside the pants that you were wearing and, subsequently, when you were taken to hospital, a further 65 pellets of heroin were discharged from your body.
     </p>
     <p>
      You told the police, in a record of interview, that you had been recruited by a person called ‘Mike’ in Mumbai to collect the drugs from Delhi and bring them to Hong Kong.  In Delhi, you met another male called ‘Joe’ who gave you the pellets to swallow, which you did, and you then brought them to Hong Kong.  For this, you were to be paid US$5,000 for successful delivery to Hong Kong.
     </p>
     <p>
      I have read the letter that you have written to me and which has been handed to me by your counsel Mr Whitehouse.  It makes for tragic reading.  You are 48 years of age now, of clear record, a single mother, having three children of your own.  You also, I understand, have the responsibility of looking after seven other children, four nephews and three nieces.  These are children of your two sisters, both of whom, together with their respective husbands, have now died of Aids.
     </p>
     <p>
      In addition to this, to add to your overwhelming difficulties, your shop and your home were burnt down during the post-election riots that took place in Kenya at the end of 2007.  As a result of your desperate situation, you say yourself in the letter, you were easy prey to the marauding drug bosses who brought you into their cartel.
     </p>
     <p>
      I am asked by your counsel to take all of these matters into account in sentencing you.  I will do so and I will also give you credit for your plea of guilty to this offence, which is an indication of your genuine remorse.
     </p>
     <p>
      I must, however, also bear in mind that there is an aggravating feature here and that is that there is, quite obviously, an international element to this offence in the sense that this large quantity of drugs was brought into Hong Kong by yourself from overseas.
     </p>
     <p>
      The sentencing guidelines contained in
      <u>
       Regina v Lau Tak Ming &amp; Others
      </u>
      (1990)
      <a href="http://www.austlii.edu.au/cgi-bin/LawCite?cit=2 HKLR 370">
       2 HKLR 370
      </a>
      puts you just outside the 15 to 20-year starting point bracket, as you had in your possession over 600 grammes of heroin.  I am prepared, however, to invoke a starting point that keeps you within that sentencing bracket but, due to the aggravating feature that I have referred to, I find that I am unable to adopt a starting point of less than 20 years’ imprisonment.
     </p>
     <p>
      Indeed, I do adopt that as my starting point.  I will discount that starting point by one-third to take account of your plea of guilty, coming to 13 years 4 months’ imprisonment.
     </p>
     <p>
      In addition, and as an act of mercy, I will give you a further discount of 16 months’ imprisonment to take account of the tragic circumstances that you found yourself in, leading you to commit this offence, arriving at a sentence of 12 years’ imprisonment.
     </p>
     <p>
      <b>
      </b>
     </p>
    </td>
   </tr>
  </table>
 </form>
</body>"""