%let wrds=wrds-cloud.wharton.upenn.edu 4016;
options comamid=TCP remote=WRDS;
signon username=_prompt_;
Libname rwork slibref=work server=wrds;


rsubmit;
libname spr "/wrdslin/comp/sasdata/nam/rating";
proc contents data=spr.adsprate;
run;

endrsubmit;


rsubmit;
data adsprate;
set spr.adsprate;
if splticrm ^= " ";
run;

endrsubmit;


rsubmit;
data comp;
set comp.funda;
if INDFMT= "INDL" & CONSOL = "C" & POPSRC ="D"  & DATAFMT ="STD";
run;


proc sql;
create table rating 
as select a.*,b.splticrm
from comp as a join adsprate as b
on a.gvkey = b.gvkey and a.datadate = b.datadate;
quit;
proc download data=rating out=rating ;run;

endrsubmit;


proc export data=rating  
outfile="C:\Users\shaox201\Dropbox\xys\classes\murray2018\FINA8823_ML\data\ratings.csv" 
dbms=csv replace;
run;

proc freq data=rating;
table splticrm;
run;

/*96.68% are B- or higher*/
data rating;
set rating;
if splticrm eq "AAA" or splticrm eq "AA+" or splticrm eq "AA" 
or splticrm eq "AA-" or splticrm eq "A+" or splticrm eq "A" or splticrm eq "A-" 
or splticrm eq "BBB+" or splticrm eq "BBB" or splticrm eq "BBB-" 
then junk_flag=0;
else junk_flag=1;
run;


proc freq data=rating;
table junk_flag;
run;

data rating;
set rating;
if xi = . then xi = 0;
if do = . then do = 0;
if acchg = . then acchg = 0;
if spi = . then spi = 0;
if rdipa = . then rdipa = 0;
if rca = . then rca = 0;
if gla = . then gla = 0;
if seta = . then seta = 0;
if aqa = . then aqa = 0;
if gdwlia = . then gdwlia = 0;
if wda = . then wda = 0;
if dtea = . then dtea = 0;
if spioa = . then spioa = 0;
if rdip = . then rdip = 0;
if rcp = . then rcp = 0;
if glp = . then glp = 0;
if setp = . then setp = 0;
if aqp = . then aqp = 0;
if gdwlip = . then gdwlip = 0;
if wdp = . then wdp = 0;
if dtep = . then dtep = 0;
if spiop = . then spiop = 0;
if seq = . then delete;
if txditc = . then txditc = 0;
if pstk = . then pstk = 0;
*set the missing to 0 for the income statement variables;
if txt = . then txt = 0;
if dp = . then dp = 0;
if xint = . then xint = 0;
bv = seq + txditc - pstk;
mv = csho*prcc_f;
if txdb =. then txdb = 0 ; if itcb = . then itcb = 0;
PS = coalesce(PSTK,PSTKL,PSTKRV,0);
se = coalesce(seq, sum(ceq, ps), at-lt);
Bv2 = SE-PS+txdb+itcb;
mtb = mv/bv;
btm = bv/mv;
mtb2 = mv/bv2;
if dlc = . then dlc = 0;
if dltt = . then dltt = 0;
dta = (dlc + dltt)/at;
bleverage = (dlc + dltt)/(dlc + dltt + bv);
mleverage = (dlc + dltt)/(dlc + dltt + mv);
size = log(at);
if xidoc = . then xidoc = 0;
rename ni = e;
ic = ppent + act - lct + ch;
run;


proc corr data=rating;
var junk_flag bleverage mleverage size btm;
run;
