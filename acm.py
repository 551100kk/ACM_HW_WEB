import urllib
import datetime
from urllib import request

user_url_list = ['http://acm.csie.org/ntujudge/user_info.php?user_id=851',
			'http://acm.csie.org/ntujudge/user_info.php?user_id=880',
			'http://acm.csie.org/ntujudge/user_info.php?user_id=919',]

hw_url_list = ['http://acm.csie.org/ntujudge/contest_index.php?contest_id=450',
			'http://acm.csie.org/ntujudge/contest_index.php?contest_id=452',
			'http://acm.csie.org/ntujudge/contest_index.php?contest_id=454',
			'http://acm.csie.org/ntujudge/contest_index.php?contest_id=457',
			'http://acm.csie.org/ntujudge/contest_index.php?contest_id=460',
			'http://acm.csie.org/ntujudge/contest_index.php?contest_id=463',
			'http://acm.csie.org/ntujudge/contest_index.php?contest_id=464',
			'http://acm.csie.org/ntujudge/contest_index.php?contest_id=467',
			'http://acm.csie.org/ntujudge/contest_index.php?contest_id=469',
			'http://acm.csie.org/ntujudge/contest_index.php?contest_id=472',
			'http://acm.csie.org/ntujudge/contest_index.php?contest_id=474',
			'http://acm.csie.org/ntujudge/contest_index.php?contest_id=478',
			'http://acm.csie.org/ntujudge/contest_index.php?contest_id=481',]

user_id = ['Jerry', 'Kevin', 'Joe']
user_cnt = [0,0,0]
pro_list = []
hw_list = []

# find solved problems
for url in user_url_list:
	response = urllib.request.urlopen(url, timeout=5)  
	html = str(response.read())
	idx = 0
	arr = []
	while True:
		sttr = "problem.php?id="
		lenn = len(sttr)
		idx = html.find(sttr, idx)
		if idx == -1:
			break

		idx = html.find("</b>", idx)
		prob = html[idx - 4 : idx]
		idx = idx + lenn + 4
		arr.append(prob)

	pro_list.append(arr)

# find homework problem
for url in hw_url_list:
	response = urllib.request.urlopen(url, timeout=5)  
	html = str(response.read())
	idx = 0
	arr = []
	while True:
		sttr = "problem.php?id="
		lenn = len(sttr)
		idx = html.find(sttr, idx)
		if idx == -1:
			break

		idx = html.find('"', idx)
		prob = html[idx - 4 : idx]
		idx = idx + lenn + 4
		idd = ""
		for i in range(len(prob)):
			x = prob[i]
			if(ord(x) > ord('9') or ord(x) < ord('0')):
				idd += '0'
			else :
				idd += x
		arr.append(idd)

	hw_list.append(arr)

# html
time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
time = str(time)
html = '''
<html>
<head><title>ACM \OAO/ Homework</title><meta charset="UTF-8"><link href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet"><style type="text/css">body {
  margin: 3em;
}
.ac{
	color: green;
}
.wa{
	color: red;
}
th{
	width: 4%;
}
td{
	width: 4%;
}
</style></head>
</html>
<body data-gr-c-s-loaded="true">
	<h2>ACM 2016 HW</h2>
	<p class="text-success">Generated @'''
html += time + ' </p>'

cnt = 1
pro_cnt = 0
status = ['wa', 'ac']
for x in hw_list:
	table = ''
	# table head
	table += '''
	<div class="table-responsive">
		<table class="table">
			<thead>
				<tr>'''
	table += '<th>HW%d</th>' % cnt
	cnt += 1
	user = []
	total = 0

	for y in x:
		flag = 0
		check = []
		for i in range(3):
			if y in pro_list[i]:
				check.append(1)
				flag = 1
			else:
				check.append(0)
		user.append(check)
		total += flag
		table += '<th class="text-center"><a class="%s" href="http://acm.csie.org/ntujudge/problem.php?id=%s">%s</a></th>\n' % (status[flag], y, y)
	table += '''<th class="text-center">AC</th>
				</tr>
			</thead>
'''
	#table body

	table += '''
			<tbody>
				<tr><td></td>
'''
	for i in range(10):
		who = ''
		for j in range(len(user[i])):
			if user[i][j] == 1:
				user_cnt[j] += 1
				who += '%s<br>' % user_id[j]
		table += '<td class="text-center">%s</td>\n' % who
	table += '<td class="text-center">%d</td>\n' % total
	table += '''
				</tr>
			</tbody>
		</table>
	</div>
'''
	#end
	html += table
	pro_cnt += total
	#break

html += '''
<h4><strong>AC:		%d</strong></h4>
<h4><strong>Remain:	%d</strong></h4>
<h4><strong>Jerry:	%d</strong></h4>
<h4><strong>Kevin:	%d</strong></h4>
<h4><strong>Joe:	%d</strong></h4>
</body>
</html>
''' % (pro_cnt, 10 * len(hw_url_list) - pro_cnt, user_cnt[0], user_cnt[1], user_cnt[2])

print (html)