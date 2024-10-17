---
layout: post
title:  "Wise bits"
date:   2023-05-28 00:42:07 +0300
categories: kotlin
---
&nbsp;&nbsp; Short observation related to bitwise operations.  
&nbsp;&nbsp; Frankly, I'm not using them very often, but occasionally decided to measure performance difference between regular `pow` operation and bitwise `<<<`, because heard multiple times that bitwise operations perform better.  
&nbsp;&nbsp; So, here are two samples:  
* power of 2 using multiplication in loop (and example with Math.pow() for comparison)
{% highlight java %}
  @Benchmark
  fun pow2(){
  var result = 1
  for (i in 1..power){
  result *= 2
  }
  }

  @Benchmark
  fun pow2Math(){
  Math.pow(2.0, power.toDouble())
  }
{% endhighlight %}

* the same power of 2 using left unsigned shift  
{% highlight java %}
fun pow2bitwise(){
  //        This line equals 2^power
  1 shl power
}
{% endhighlight %}  
&nbsp;&nbsp; [The whole benchmark is here](https://github.com/dzmitrykashlach/algorithms-storehouse/blob/main/benchmarks/src/main/kotlin/bitwise/BitwiseBenchMark.kt)  
&nbsp;&nbsp; Here are results of benchmark (pretty expected)  
```
main summary:
Benchmark                      (power)  Mode  Cnt        Score        Error  Units
BitwiseBenchMark.pow2           100000  avgt    3    24025.646 ±   2150.133  ns/op
BitwiseBenchMark.pow2         10000000  avgt    3  2391201.922 ± 199229.741  ns/op
BitwiseBenchMark.pow2Math       100000  avgt    3        8.757 ±      0.668  ns/op
BitwiseBenchMark.pow2Math     10000000  avgt    3        8.750 ±      0.455  ns/op
BitwiseBenchMark.pow2bitwise    100000  avgt    3        0.353 ±      2.009  ns/op
BitwiseBenchMark.pow2bitwise  10000000  avgt    3        0.356 ±      2.031  ns/op
```  
* my ugly function with loop gives worse performance: __O(n)__ time complexity
* `Math.pow()` performs better and shows __O(1)__ complexity
* left shift `<<<` is faster than everything above.

&nbsp;&nbsp; Hope, it was interesting to know. See you! :-)



