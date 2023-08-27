<template>
  <div id="web">
    <header>
      <h2>MTD Simulator</h2>
    </header>

  <div id="container">
    <section class="content">
      <div class="scroll">
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
      </div>
  
  
      <article>
        <h1>Network Display</h1>
      </article>
      </section>

      <footer>
      </footer>
    </div>
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

#app{
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow: hidden;
}

.content{
  display: flex;
  flex: 1;
}

div.scroll{
  float: left;
  width: 30%;
  background: #ccc;
  padding: 20px;
  overflow: auto;
  max-height: calc(100vh - 10px);
}

article {
  float: left;
  padding: 20px;
  width: 70%;
  height: auto;
  text-align: center;
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
  flex: 1;
  overflow: auto;
}

footer {
  flex-shrink: 0;
  background-color: #777;
  text-align: center;
  color: white;
  bottom: 0;
  padding: 10px;
}

@media (max-width: 600px) {
  form, article {
    width: 100%;
    height: auto;
  }
}

</style>