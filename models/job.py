class Job:
  def __init__(self, link, title, company, experience, reward):
    self.link = link
    self.title = title
    self.company = company
    self.experience = experience
    self.reward = reward

  def __str__(self):
    return f"link: {self.link}, title: {self.title}, company: {self.company}, experience: {self.experience}, reward: {self.reward}"
  