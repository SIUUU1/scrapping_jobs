def save_to_file(file_name, all_jobs):
   file = open(f"{file_name}.csv", "w")
   file.write("Link, Title, Company, Experience, Reward \n")

   for job in all_jobs:
     file.write(f"{job.link}, {job.title}, {job.company}, {job.experience}, {job.reward} \n")

   file.close()
