import re

import bert
import nltk
import numpy as np
import pandas as pd
import tensorflow as tf
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.tokenize.punkt import PunktParameters

# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')

VOCAB_FILE = 'bert_uncased_L-12_H-768_A-12/assets/vocab.txt'

def cleanUpSentence(r):
    strip_special_chars = re.compile("[^A-Za-z0-9, ]+")
    r = r.lower().replace("<br />", " ")
    r = re.sub(strip_special_chars, "", r.lower())
    words = word_tokenize(r)
    filtered_sentence = []
    for w in words:
        if any(map(str.isdigit, w)):
            filtered_sentence.append("0")
        elif w:
            filtered_sentence.append(w)
    return " ".join(filtered_sentence),len(filtered_sentence)


def clean_data(datas_X):    
    totalX = []
    maxLength = 0
    for i, doc in enumerate(datas_X):
        doc = doc.replace("\n"," ")
        sent,sent_len = cleanUpSentence(doc)
        maxLength = max(maxLength,sent_len)
        totalX.append(sent)
    totalX=np.array(totalX)
    return totalX

def get_paras(content):
    segmented_sign = re.compile('(\n[ ]*){2,}')
    all_sign = segmented_sign.finditer(content)
    paras,last_start = [],0
    for sign in all_sign:
        paras.append((last_start,sign.span()[0]-1))
        last_start = sign.span()[1]
    paras.append((last_start,len(content)-1))
    return paras

def convert_sentence_to_features(sentence, tokenizer, max_seq_len):
    tokens = ['[CLS]']
    tokens.extend(tokenizer.tokenize(sentence))
    if len(tokens) > max_seq_len-1:
        tokens = tokens[:max_seq_len-1]
    tokens.append('[SEP]')
    
    segment_ids = [0] * len(tokens)
    input_ids = tokenizer.convert_tokens_to_ids(tokens)
    input_mask = [1] * len(input_ids)

    #Zero Mask till seq_length
    zero_mask = [0] * (max_seq_len-len(tokens))
    input_ids.extend(zero_mask)
    input_mask.extend(zero_mask)
    segment_ids.extend(zero_mask)
    
    return input_ids, input_mask, segment_ids

def convert_all_sentences(sentences, tokenizer, max_seq_len=267):
    all_input_ids = []
    all_input_mask = []
    all_segment_ids = []
    for sentence in sentences:
        input_ids, input_mask, segment_ids = convert_sentence_to_features(sentence, tokenizer, max_seq_len)
        all_input_ids.append(input_ids)
        all_input_mask.append(input_mask)
        all_segment_ids.append(segment_ids)
    return np.array(all_input_ids), np.array(all_input_mask), np.array(all_segment_ids)

def add_important_class(html_content, s, e):
    return html_content[:s] + '<div class = "important">' + html_content[s:e] + '</div>' + html_content[e:]

def get_important_sent(html_content):
    punkt_param = PunktParameters()
    punkt_param.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'miss', 'prof', 'inc','no','cap','nos','vol','para','exh'])
    tokenizer = nltk.PunktSentenceTokenizer(punkt_param)
    soup = BeautifulSoup(html_content, 'html.parser')
    content = soup.get_text()
    paras = get_paras(content)
    sents = []
    for para in paras:
        para_content = content[para[0]:para[1]+1]
        for sent in tokenizer.span_tokenize(para_content):
            sents.append(para_content[sent[0]:sent[1]+1])
    sents = np.array(sents)
    BertTokenizer = bert.bert_tokenization.FullTokenizer(VOCAB_FILE,do_lower_case=True)
    input_ids, input_mask, segment_ids = convert_all_sentences(clean_data(sents), BertTokenizer)
    model = tf.keras.models.load_model("bert_model")
    input_X = {
        "input_ids": input_ids,
        "input_mask": input_mask,
        "segment_ids": segment_ids
    }
    sents = sents[(model.predict(input_X, batch_size = 1) > 0.4).reshape(-1,)]
    for sent in sents:
        segs = filter(lambda seg: seg != "", sent.split("\n"))
        for seg in segs:
            seg = seg.replace("\xa0","&nbsp;")
            while seg:
                cur = len(seg)
                while True:
                    if not cur:
                        return html_content
                    cur_str = seg[:cur]
                    res = html_content.find(cur_str)
                    if res == -1:
                        cur -= 1
                    else:
                        html_content = add_important_class(html_content, res, res+len(cur_str))
                        seg = seg[cur:]
                        break
    return html_content
        
html = get_important_sent("""
<body><form name=search_body><table width="100%" border="0" cellpadding="0" cellspacing="0"><tr><td>
    <p style="text-align:right">CACV 195/2017</p>

    <p style="text-align:right">[2018] HKCA 14</p>

    

    <p style="text-align:center">IN THE HIGH COURT OF THE</p>

    <p style="text-align:center">HONG KONG SPECIAL ADMINISTRATIVE REGION</p>

<p style="text-align:center">COURT OF APPEAL</p>

    <p style="text-align:center">CIVIL APPEAL NO 195 OF 2017</p>

    <p style="text-align:center">(ON APPEAL FROM HCAL NO 139 of 2017)</p>

    <p style="text-align:center">__________________________</p>
    <parties>
<table width="100%" border="0">
  <tr> 
    <td width="25%" style="text-align:center" valign="top">RE:</td>
    <td width="50%" style="text-align:center" valign="top">ZUNARIYAH</td>
    <td width="25%" style="text-align:center" valign="top">Applicant</td>
  </tr>
  </table>
</parties>

     <p style="text-align:center">__________________________</p> 

<coram>
<table width="100%">
	<tr>                
    <td width="15%" valign="top" class="auto-style1">Before:  Hon Cheung CJHC and Lam VP in Court  </td>   
	</tr>
  </table>
</coram>    
<date>
<table width="100%">
  <tr><td width="15%" valign="top" class="auto-style1">Date of Hearing:  9 January 2018</td>
   </tr>
  <tr>
    <td valign="top" class="auto-style1">Date of Judgment: 11 January 2018</td>
  </tr>
</table>
</date>

  


<p style="text-align:center">________________</p>

    <p style="text-align:center">JUDGMENT</p>

    <p style="text-align:center">________________</p>

    <p><strong>Hon Lam VP</strong> (giving the Judgment of the Court):</p>

    <p><a name="p1" class="para" id="p1">1.</a>&nbsp;&nbsp;This is an appeal against the decision of Anthony Chan J on 18 August 2017 refusing leave to the applicant to apply for judicial review. The applicant came from Indonesia to work in Hong Kong as a foreign domestic helper from July 2004 to August 2011. In respect of her last contract of employment, she arrived in Hong Kong on 6 March 2011 and was granted permission to remain until 20 July 2012 or two weeks after the termination of her employment as foreign domestic helper. That employment was terminated early. She was granted extension to stay on visitor condition until 14 September 2011. Since 15 September 2011, she overstayed beyond the permission to remain here granted by the Director of Immigration. She surrendered herself on 22 September 2011.</p>

    <p><a name="p2" class="para" id="p2">2.</a>&nbsp;&nbsp;She had formed a relationship with a man Abbas Raza [“AR”] in Hong Kong whilst working as a foreign domestic helper and they had a “nikah siri” ceremony on 2 May 2010 at a mosque in Hong Kong.&nbsp; The marriage was not registered.&nbsp; On 18 October 2011, she gave birth to a daughter for AR.</p>

    <p><a name="p3" class="para" id="p3">3.</a>&nbsp;&nbsp;On 25 February 2014 she lodged a non-refoulement claim for herself and one for her daughter.&nbsp; The claims were based on threats from her former husband (whom she had divorced in 2007), her family members in Indonesia, and the religious group in her native village regarding her union with AR.&nbsp;</p>

    <p><a name="p4" class="para" id="p4">4.</a>&nbsp;&nbsp;The Director decided against the claims on 12 November 2015. The decision covered BOR 3 risk, persecution risk and torture risk.&nbsp; By a supplemental decision of 20 October 2016, the Director also assessed BOR 2 risk in respect of the applicant and her daughter and decided against them.</p>

    <p><a name="p5" class="para" id="p5">5.</a>&nbsp;&nbsp;The applicant and her daughter appealed to the Torture Claims Appeal Board.&nbsp; After a hearing held on 7 November 2016, the Board dismissed the appeals on 15 March 2017.</p>

    <p><a name="p6" class="para" id="p6">6.</a>&nbsp;&nbsp;The intended judicial review was in respect of the decision of the Torture Claims Appeal Board of 15 March 2017.&nbsp; The Form 86 filed by the applicant on 13 April 2017 did not contain any grounds for seeking relief.&nbsp; In her affirmation of 13 April 2017, she simply deposed as follows:</p>

    <blockquote>
        <p class="quote">“ I want to seek for judicial review for my claims after I dismissed my appeal by Torture Claims Appeal Board because I have problems with my family members, my ex-husband and also religious people in my place and I scared to go back home to Indonesia they will treats and prosecution me and my childs.”</p>
    </blockquote>

    <p><a name="p7" class="para" id="p7">7.</a>&nbsp;&nbsp;The papers of the application were first placed before Patrick&nbsp;Li&nbsp;J as the judge designated to co-ordinate leave applications from unrepresented torture claim applicants.&nbsp; His Lordship noted that the applicant did not include the written decisions of the Director and the written decision of the Board in the papers lodged by her.&nbsp; The judge therefore called for those documents from the Director of Immigration to facilitate the processing of the application.</p>

    <p><a name="p8" class="para" id="p8">8.</a>&nbsp;&nbsp;Though an application for leave to apply for judicial review is made <i>ex parte</i>, the judge processing the application has the power to call for relevant documents or initial response from a putative respondent, see <i>Re Leung Kwok Hung</i> HCAL 83 of 2012, 28 September 2012 at [33] to [45]; <i>MST v Duty Lawyer Service</i> CACV 179 of 2013, 3 July 2015.&nbsp; The extent to which the court needs to exercise such power is a matter of case management and the objective is to facilitate the court in the efficient and effective performance of its filtering role in a leave application.</p>

    <p><a name="p9" class="para" id="p9">9.</a>&nbsp;&nbsp;In the present context, the Form 86 and supporting affirmation of the applicant plainly did not give adequate information to the court.&nbsp; P&nbsp;Li&nbsp;J had to obtain copies of the decisions in order to process the leave application.&nbsp; One option was to direct the applicant to produce the same. Bearing in mind that the applicant was unrepresented with limited resources, there could be further delays.&nbsp; In such circumstances, it was legitimate for the judge to request such documents from the putative respondent, the Director of Immigration.</p>

    <p><a name="p10" class="para" id="p10">10.</a>&nbsp;&nbsp;After the decisions were available, P Li J transferred the case to Anthony Chan J.&nbsp; Hence, by the time Anthony Chan J got the papers, the written decisions of the Director and the Board were in the court file.&nbsp;&nbsp;&nbsp;</p>

    <p><a name="p11" class="para" id="p11">11.</a>&nbsp;&nbsp;The judge gave very brief reasons in refusing leave.&nbsp; They were set out in the CALL-1 Form:</p>

    <blockquote>
        <p class="quote">“ I am unable to see any merit in this application.&nbsp; Neither the Form 86 nor the supporting affirmation contain any particulars or supporting document. More importantly, Ms Zunariyah’s “fear” for her safety is not properly grounded.&nbsp; Her case (and that of her daughter) had been carefully considered by the 2 decision makers in question.&nbsp; Leave is refused.”</p>
    </blockquote>

    <p><a name="p12" class="para" id="p12">12.</a>&nbsp;&nbsp;In the notice of appeal of 30 August 2017, the applicant advanced two grounds of appeal:</p>

    <blockquote>
        <p>(a)&nbsp;&nbsp;&nbsp;There was inconsistency in the judge’s observations on the lack of particulars or supporting document in the Form 86 and supporting affirmation and his reference to the written decisions of the Director and the Board; and</p>

        <p>(b)&nbsp;&nbsp;&nbsp;She did not have legal representation in the Board and in the application for judicial review application and this violates the principle of high standard of fairness laid down in <i>Sakthevel Prabakar v Secretary for Security</i> (2004) 7 HKCFAR 187.&nbsp; She also complained about lack of interpretation services.</p>
    </blockquote>

    <p><a name="p13" class="para" id="p13">13.</a>&nbsp;&nbsp;She lodged written submissions (dated 10 December and received by the court on 12 December) in support of her appeal.&nbsp; In those submissions, written in English (like all the documents she placed before us), she reiterated those grounds and cited <i>FB v Director of Immigration</i> HCAL 51 of 2007.</p>

    <p><a name="p14" class="para" id="p14">14.</a>&nbsp;&nbsp;By a letter of 1 September 2017, the applicant agreed to have the appeal heard by 2 judges instead of 3 judges.&nbsp; We heard the appeal on 9&nbsp;January 2017.</p>

    <p><a name="p15" class="para" id="p15">15.</a>&nbsp;&nbsp;We do not see any merit in the appeal.&nbsp; Given the history in the conduct of the proceedings as set out above, there is no inconsistency in the judge’s observation.</p>

    <p><a name="p16" class="para" id="p16">16.</a>&nbsp;&nbsp;As regards legal representation and interpretation services, these are not grounds advanced at the court below.&nbsp; In general, an appeal is not the occasion for fresh grounds to be advanced and in the absence of good reason, an appellant should be confined to the materials she had placed before the court below.&nbsp; In the context an appeal against refusal to grant leave for judicial review, this principle is applicable because the relaxation of this principle too readily would be inconsistent with the strict time limit and the duty of promptitude in the overall scheme of rules for bringing judicial review.</p>

    <p><a name="p17" class="para" id="p17">17.</a>&nbsp;&nbsp;In any event, the ground has no merit.&nbsp; The applicant did not explain why she did not have the service of duty lawyer when she appealed to the Board.&nbsp; Before the Director, she had been represented by the Duty Lawyer Service as the Notice of Decision of 12 November 2015 was sent to the applicant through them.</p>

    <p><a name="p18" class="para" id="p18">18.</a>&nbsp;&nbsp;As a standard practice, the Director would have drawn her attention to the Duty Lawyer Service and asked her to contact them as soon as possible. The Duty Lawyer Service provided legal representation in appeal to the Board for cases with merit. Neither <i>Sakthevel Prabakar v Secretary for Security</i> (2004) 7 HKCFAR 187 nor <i>FB v Director of Immigration</i> HCAL 51 of 2007 prescribed that a CAT claimant or a claimant for BOR 2 or BOR 3 or persecution risks must have an absolute right to free legal representation <u>at all stages</u> of the proceedings. The claimant already had the benefit of legal representation in presenting her case to the Director of Immigration including presence of lawyer at the interview by the immigration officer. Duty lawyer service is available for the appeal proceedings though it is subject to a merit test. &nbsp;&nbsp;&nbsp;</p>

    <p><a name="p19" class="para" id="p19">19.</a>&nbsp;&nbsp;In the absence of any assertion by the Applicant that the merit test had not been properly applied, it does not lie in her mouth to complain of the lack of legal representation in the proceedings before the Board.</p>

    <p><a name="p20" class="para" id="p20">20.</a>&nbsp;&nbsp;Interpretation services are provided at hearings before the Board if the same was requested by an applicant. The Applicant did not state if she had requested for such services. Nor did she highlight any particular aspect of the proceedings before the Board where the lack of interpretation service hampered her presentation of her appeal.&nbsp;&nbsp;&nbsp;&nbsp;</p>

    <p><a name="p21" class="para" id="p21">21.</a>&nbsp;&nbsp;The applicant did not agree with the judge’s brief observations in the CALL-1 Form.&nbsp; Those observations should be read together with the detailed reasons given by the Board as well as the Notices of Decision of the Director. It should also be read in light of the minimal materials put forward by the applicant in her Form 86 and affirmation lodged to support her application.&nbsp;</p>

    <p><a name="p22" class="para" id="p22">22.</a>&nbsp;&nbsp;It must be emphasized that in a judicial review, even in the context of a case of this nature, the court does not usurp the role of the primary decision maker.&nbsp; The court’s duty is to consider the legality, rationality and procedural fairness of the proceedings before the Director and the Board.&nbsp; Thus, even though the court should examine if the procedure adopted by the primary decision maker conforms with the high standard of fairness, the court should not intervene if the materials produced by an applicant do not reveal any ground to impinge the legality, rationality or fairness of the process below.&nbsp; An applicant must produce something to satisfy such threshold before leave to apply for judicial review can be granted.&nbsp;</p>

    <p><a name="p23" class="para" id="p23">23.</a>&nbsp;&nbsp;Leave application is meant to be a filtering process and the judge is not expected to give elaborated reasons for his decision.&nbsp; Having considered the submissions of the applicant in light of the materials before us, we find the judge’s observations to be justified.&nbsp; We do not see any errors of law or procedures in the proceedings before the Board and there is no reasonably arguable basis to challenge the fairness of the process.&nbsp; We agree with the judge that leave to apply for judicial review should not be granted.</p>

    <p><a name="p24" class="para" id="p24">24.</a>&nbsp;&nbsp;For these reasons, we do not see any prospect of success in the intended application for judicial review and we dismiss the appeal accordingly.</p>
	<p>&nbsp;&nbsp;</p>
	<p>&nbsp;&nbsp;</p>
<table width="100%" border="0">
  <tr>
    <td width="50%" style="text-align:center">(Andrew Cheung)</td>
    <td width="50%" style="text-align:center">(M H Lam)</td>
  </tr>
  <tr>
    <td style="text-align:center">Chief Judge of</td>
    <td style="text-align:center">Vice President</td>
  </tr>
  <tr>
    <td style="text-align:center">the High Court</td>
    <td style="text-align:center">&nbsp;</td>
  </tr>
</table>

<representation><p>&nbsp;&nbsp;</p>
	<p>The applicant appearing in person</p></representation>
	<p>&nbsp;&nbsp; </p>
</td></tr></table></form></body>""")
