<template>
    <header>
  <h2>MTD Simulator</h2>
</header>

<div id="container">
  <section>
  <form>
    <h2> Parameters Panel</h2>

    <label>Number of Nodes: </label>
    <input type="text" placeholder="Number of Nodes...">

    <label>Number of Nodes: </label>
    <input type="text" placeholder="Number of Nodes...">

    <label>Number of Nodes: </label>
    <input type="text" placeholder="Number of Nodes...">

    <label>Number of Nodes: </label>
    <input type="text" placeholder="Number of Nodes...">

    <label>Number of Nodes: </label>
    <input type="text" placeholder="Number of Nodes...">

    <label>Number of Nodes: </label>
    <input type="text" placeholder="Number of Nodes...">

    <label>Number of Nodes: </label>
    <input type="text" placeholder="Number of Nodes...">

    <label>Number of Nodes: </label>
    <input type="text" placeholder="Number of Nodes...">

    <label>Number of Nodes: </label>
    <input type="text" placeholder="Number of Nodes...">

    <label>Number of Nodes: </label>
    <input type="text" placeholder="Number of Nodes...">

    <label>Number of Nodes: </label>
    <input type="text" placeholder="Number of Nodes...">

    <label>Number of Nodes: </label>
    <input type="text" placeholder="Number of Nodes...">

    <label>Number of Nodes: </label>
    <input type="text" placeholder="Number of Nodes...">

    <label>Number of Nodes: </label>
    <input type="text" placeholder="Number of Nodes...">

    <label>Number of Nodes: </label>
    <input type="text" placeholder="Number of Nodes...">

    

    <input type="submit" value="Submit">

  </form>
  
  <article>
    <h1>Network Display</h1>
  </article>
  </section>

  <footer>
    <p>Footer</p>
  </footer>
</div>


</template>

<script>
export default {
  name: 'MTDSimulator',
}
</script>

<style>
  * {
  box-sizing: border-box;
}


header {
  background-color: rgb(12, 69, 225);
  padding: 30px;
  text-align: center;
  font-size: 35px;
  color: white;
}

form {
  float: left;
  width: 30%;
  background: #ccc;
  padding: 20px;
  position: static;
}

article {
  float: left;
  padding: 20px;
  width: 70%;
  background-color: #f1f1f1;
  height: auto;
}

input[type=text] {
   width: 100%;
   margin: 5px 0 10px 0;
   display: inline-block;
   border: none;
   background: #f1f1f1;
}

input[type=text]:focus {
   background-color: #ddd;
   outline: none;
}

#container{
  position: relative;
  min-height: 100vh;
}

footer {
  background-color: #777;
  padding: 20px;
  text-align: center;
  color: white;
  position: absolute;
  bottom: 0;
  width: 100%;
}

@media (max-width: 600px) {
  form, article {
    width: 100%;
    height: auto;
  }
}

</style>