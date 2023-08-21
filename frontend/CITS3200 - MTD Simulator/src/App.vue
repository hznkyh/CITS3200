<template>
  <div class="navbar">
    <img class="logo" src="CITS3200\CITS3200 - MTD Simulator\src\components\icons\logo.jpg">
    <a href="#/">Home</a>
    <a href="#/mtd simulator">MTD Simulator</a>
    <component :is="currentView"/>
  </div>
  <home/>
  <mtd-simulator/>
</template>

<script>
</script>

<style>
  body{
    margin: 0;
  }
  
  .navbar {
    width: 100%;
    background-color: #173590;
    overflow: auto;
  }

  .navbar a {
    float: left;
    text-align: center;
    padding: 12px;
    color: white;
    text-decoration: none;
    font-size: 20px;
  }

  .navbar a:hover {
    background-color: #000;
  }

  @media screen and (max-width: 500px) {
    .navbar a {
      float: none;
      display: block;
    }
  }

  .logo{
    height: auto;
    width: auto;
    float: left;
    padding-left: 2%;
    margin: 0 auto;
    padding-right: 20px;
  }
</style>
