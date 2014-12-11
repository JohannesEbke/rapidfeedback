if (manager.build.result.isWorseThan(hudson.model.Result.SUCCESS)) {
  def culprits = manager.build.getCulprits()
  if (!culprits.isEmpty()) {
    def culprit = culprits.iterator().next()
    def myURL = "http://10.8.0.205:6666/fire_at/" + culprit.getId()
    def connection = new URL(myURL).openConnection()
    connection.setDoOutput(true); // Triggers POST.
    connection.getOutputStream().write("A Rocket".getBytes())
    println connection.getInputStream().getText()
  }
}
