from agithub.GitHub import GitHub
import json
import csv
import os

def pull_requests(g):
	pull_dict={}
	with open('list.csv', newline='') as csvfile:
		spamreader = csv.reader(csvfile)
		i = 0
		for row in spamreader:
			print(row)
			status ,data = g.repos[row[1]].pulls.get()
			y =json.dumps(data,indent=2)
			z= json.loads(y)
#Finding latest pull request
			max = 0
			for item in z:
				if(item.get("number")>max):
					max = item.get("number")
			for item in z:
				if(item.get("number")== max):
					pull_dict[i] = {}
					pull_dict[i]['title']= item.get("title")
					pull_dict[i]['state']= item.get("state")
					pull_dict[i]['created_at']= item.get("created_at")
					pull_dict[i]['updated_at']= item.get("updated_at")
					break
			i= i+1
	print(pull_dict)
	return pull_dict
#Fetching Iusses
def issues(g):
	details_dict={}
	with open('list.csv', newline='') as csvfile:
		spamreader = csv.reader(csvfile)
		i = 0
		for row in spamreader:
			status ,data = g.repos[row[1]].issues.get()
			y =json.dumps(data,indent=2)
			z= json.loads(y)
#finding latest issue
			max = 0
			for item in z:
				if(item.get("number")>max):
					max = item.get("number")
			for item in z:
				if(item.get("number")== max):
					details_dict[i] = {}
					details_dict[i]['title']= item.get("title")
					details_dict[i]['state']= item.get("state")
					details_dict[i]['created_at']= item.get("created_at")
					details_dict[i]['updated_at']= item.get("updated_at")
					break
			i= i+1
	print(details_dict)
	return details_dict
#Writing everything to "out.csv" file
def write_data(pull_dict,details_dict):
	headers = ['name','issues','title_i','state_i','created_at_i','updated_at_i','pulls','title_p','state_p','created_at_p','updated_at_p']
	x=0
	with open('list.csv', newline='') as csvfile, open('out.csv', 'a', newline='') as outfile:
		writer = csv.DictWriter(outfile, fieldnames=headers)
		writer.writeheader()
		reader = csv.reader(csvfile)
		for row in reader:
			if x in pull_dict and x in details_dict:
				writer.writerow({'name':row[0],'title_i':details_dict[x]['title'],'state_i':details_dict[x]['state'],'created_at_i':details_dict[x]['created_at'],'updated_at_i':details_dict[x]['updated_at'],'title_p':pull_dict[x]['title'],'state_p':pull_dict[x]['state'],'created_at_p':pull_dict[x]['created_at'],'updated_at_p':pull_dict[x]['updated_at']})
			elif x in pull_dict:
				writer.writerow({'name':row[0],'title_p':pull_dict[x]['title'],'state_p':pull_dict[x]['state'],'created_at_p':pull_dict[x]['created_at'],'updated_at_p':pull_dict[x]['updated_at']})
			elif x in details_dict:
				writer.writerow({'name':row[0],'title_i':details_dict[x]['title'],'state_i':details_dict[x]['state'],'created_at_i':details_dict[x]['created_at'],'updated_at_i':details_dict[x]['updated_at']})
			else:
				writer.writerow({'name':row[0]})
			x=x+1


def main():
	#Add your Github Credentials here
	git = GitHub('username', 'password')
	#Deleting out.csv if it already exists
	try:
		os.remove('out.csv')
	except OSError:
		pass 
	pulls=pull_requests(g=git)
	issue=issues(g=git)
	write_data(pull_dict=pulls,details_dict=issue)
main()