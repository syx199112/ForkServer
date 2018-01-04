#!/usr/bin/python

import random
import sys 
import math

class Server:
	def __init__(self, name):
		self.name = name
		self.departure_next_time = float("inf")
		self.arrival_time_this_departure = 0
		self.subtask_request = 0
		self.number_subtask = 0

		self.is_free = False
		self.is_busy = True
		self.queue_length = 0
		self.buffer_list = []

class Processor:
	def __init__(self):
		self.is_free = False
		self.is_busy = True
		self.queue_length = 0
		self.buffer_list = []

class Working_Server:
	def __init__(self):
		self.arrival_next_time = float("inf")

class Working_Processor:
	def __init__(self):
		self.arrival_next_time = None
		self.service_time_next_arrival = None
		self.departure_next_time = float("inf")
		self.arrival_time_next_departure = 0

def worktime(n):
	tm = 10.3846
	k = 2.08

	sub_t = (tm ** k) / (n ** (1.65 * k))
	service_time_subtask = (sub_t / (1 - random.uniform(0,1))) ** (1 / k)

	return service_time_subtask

processor = Processor()
working_processor = Working_Processor()
working_server = Working_Server()

Tend = int(input('Tend is total serve time , set Tend = '))
n = int(input('Selects n distinct servers out of m servers , set n =  '))
o = int(input('Test No.'))

T = 0
N = 0

arrival_rate = 0.85
service_rate = 10 / n
random.seed(o)

major_time = 0
joint_point_status = []
per_server_name = "server"
full_server_names = []

for i in range (1,11):
	j=per_server_name+str(i)
	full_server_names.append(j)

server_list = []

for i in full_server_names:
	server = Server(i)
	server_list.append(server)

uniformly_distributed_interval = random.uniform(0.05,0.25)
working_processor.service_time_next_arrival = random.expovariate(service_rate)	
working_processor.arrival_next_time = random.expovariate(arrival_rate) + uniformly_distributed_interval

flog_1 = False

if major_time < Tend:
	flog_1 = True
 
while flog_1:
	inciden_time = []
	paralle_inciden_time = []
	inciden_time.append(working_processor.arrival_next_time)
	inciden_time.append(working_processor.departure_next_time)

	for i in range(len(server_list)):
		inciden_time.append(server_list[i].departure_next_time)

	minimum_time = min(inciden_time)
	major_time = minimum_time

	print ("major_time: "+ str(major_time))

	for i in range(len(inciden_time)):

		if (minimum_time == inciden_time[i]):
			paralle_inciden_time.append([minimum_time, i])


	k = len(paralle_inciden_time)	

	for j in range(k):

		if(paralle_inciden_time[j][1] == 0):

			if processor.is_free:
				processor.is_busy = False
			else:
				processor.is_busy = True

			if not processor.is_free:
				working_processor.departure_next_time = working_processor.arrival_next_time + working_processor.service_time_next_arrival
				working_processor.arrival_time_next_departure = working_processor.arrival_next_time
				processor.is_free = True
			else:
				processor.buffer_list.append([working_processor.arrival_next_time, working_processor.service_time_next_arrival])
				processor.queue_length =processor.queue_length+ 1

			working_processor.arrival_next_time = major_time + random.expovariate(arrival_rate) + uniformly_distributed_interval
			working_processor.service_time_next_arrival = random.expovariate(service_rate)

		elif(paralle_inciden_time[j][1] == 1):
			arrival_time_of_this_departure_save = working_processor.arrival_time_next_departure

			if processor.queue_length:
				working_processor.departure_next_time = major_time + processor.buffer_list[0][1]
				working_processor.arrival_time_next_departure = processor.buffer_list[0][0]

				processor.buffer_list.remove(processor.buffer_list[0])
				processor.queue_length =processor.queue_length- 1

			else:
				working_processor.departure_next_time = float("inf")
				processor.is_free = False

			number_of_subtask = 1
			selected_server_list = random.sample(server_list, n)

			for server in selected_server_list:

				service_time_subtask = worktime(n)

				if server.is_free:
					server.is_busy = False
				else:
					server.is_busy = True

				if not server.is_free:
					server.departure_next_time = major_time + service_time_subtask
					server.arrival_time_next_departure = arrival_time_of_this_departure_save
					server.subtask_request = n
					server.number_subtask = number_of_subtask
					server.is_free = True
				else:
					server.buffer_list.append([arrival_time_of_this_departure_save, service_time_subtask, number_of_subtask])
					server.queue_length =server.queue_length+ 1
					
				number_of_subtask =number_of_subtask+ 1

		else:
			server_special = server_list[paralle_inciden_time[j][1] - 2]
			origianl_arrival_time = server_special.arrival_time_next_departure

			if(joint_point_status == []):
				joint_point_status.append([origianl_arrival_time, 1])
			else:
				flag_2 = False

				for k in range(len(joint_point_status)):

					if origianl_arrival_time in joint_point_status[k]:
						flag_2 = True

				if flag_2:

					for l in range(len(joint_point_status)):

						if joint_point_status[l] != [] and joint_point_status[l][0] == origianl_arrival_time:
							joint_point_status[l][1] =joint_point_status[l][1]+ 1

							if joint_point_status[l][1] == n:
								T += major_time - origianl_arrival_time
								N = N + 1
								joint_point_status[l] = []
				else:
					joint_point_status.append([origianl_arrival_time, 1])

				if (not server_special.queue_length == 0):
					server_special.departure_next_time = major_time + server_special.buffer_list[0][1]
					server_special.arrival_time_next_departure = server_special.buffer_list[0][0]
					server_special.number_subtask = server_special.buffer_list[0][2]
					server_special.buffer_list.remove(server_special.buffer_list[0])
					server_special.queue_length = server_special.queue_length - 1				
				else:
					server_special.departure_next_time = float("inf")
					server_special.is_free = False
					
		if major_time > Tend:
			flog_1 = False
		if major_time < Tend:
			flog_1 = True


print "Tend: ", Tend
print "n: ", n
print "o: ", o

print "T: ", T
print "N: ", N
Response = T/N
print "the mean response time is: : ",Response


