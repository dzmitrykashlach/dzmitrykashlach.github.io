---
layout: post
title:  "Power set: bitwise vs recursion"
date:   2023-05-22 00:00:07 +0300
categories: kotlin
---
&nbsp;&nbsp; So, [I've already written](https://dzmitrykashlach.github.io/kotlin/2023/05/27/bitwise-benchmark.html) that bitwise operations is a very fast thing. But how can this be used in application?  
Let's say, you need to iterate over the [powerset](https://en.wikipedia.org/wiki/Power_set) of some elements which can be useful in various fields (for example):
* operations with graphs;
* dynamic programming problems, where all combinations of elements should be stored in memoization table;
* other combinatorial problems...  

&nbsp;&nbsp; There are two approaches for generating powerset: recursion and bitwise operations. Which of them performs better? Let's test.
  {% highlight java %}
class PowerSet(
val set: IntArray,
) {
val subSets = mutableListOf<IntArray>()

    fun generateRecursive(at: Int, used: BooleanArray) {
        val n = set.size;
        val range = set.indices
        if (at == n) {

            // Print found subset!
            var subSet = IntArray(n)
            for (i in range) {
                if (used[i]) {
                    subSet[i] = set[i]
                }
            }
            subSets.add(subSet)
        } else {

            // Include this element
            used[at] = true
            generateRecursive(at + 1, used)

            // Backtrack and don't include this element
            used[at] = false
            generateRecursive(at + 1, used)
        }
    }

    fun generateBinary() {
        val n = set.size;
        val range = set.indices
        val maxVal = 1 shl n;

        for (subset in 0 until maxVal) {
            var subSet = IntArray(n)
            for (i in range) {
                val mask = 1 shl i
                if ((subset and mask) == mask) {
                    subSet[i] = set[i]
                }
            }
            subSets.add(subSet)
        }
    }

}
  {% endhighlight %}


{% highlight java %}
@State(Scope.Benchmark)
class PowerSetBenchmark {
@Param("3", "4", "5", "10", "20", "26")
var setSize = 0
lateinit var set: IntArray

    @Setup
    fun setUp() {
        set = IntArray(setSize) { i -> i }
    }


    @Benchmark
    fun powSetRecursive() {
        val ps = PowerSet(set)
        ps.generateRecursive(
            0, BooleanArray(setSize)
        )

    }

    @Benchmark
    fun powSetBinary() {
        val ps = PowerSet(set)
        ps.generateBinary()
    }

}
{% endhighlight %}
Source code of [PowerSet class](https://github.com/dzmitrykashlach/algorithms-storehouse/blob/main/benchmarks/src/main/kotlin/bitwise/PowerSet.kt) and [benchmark](https://github.com/dzmitrykashlach/algorithms-storehouse/blob/main/benchmarks/src/main/kotlin/bitwise/PowerSetBenchmark.kt)

__Results__  
```
Benchmark                          (setSize)  Mode  Cnt        Score         Error  Units
PowerSetBenchmark.powSetBinary             3  avgt    3        0.060 ±       0.065  us/op
PowerSetBenchmark.powSetBinary             4  avgt    3        0.137 ±       0.046  us/op
PowerSetBenchmark.powSetBinary             5  avgt    3        0.286 ±       0.064  us/op
PowerSetBenchmark.powSetBinary             9  avgt    3        6.654 ±       6.681  us/op
PowerSetBenchmark.powSetBinary            10  avgt    3       14.016 ±      18.000  us/op
PowerSetBenchmark.powSetBinary            11  avgt    3       82.002 ±      63.015  us/op
PowerSetBenchmark.powSetBinary            20  avgt    3    92927.224 ±   28005.295  us/op
PowerSetBenchmark.powSetBinary            26  avgt    3  8389329.133 ± 2665432.289  us/op
PowerSetBenchmark.powSetRecursive          3  avgt    3        0.076 ±       0.017  us/op
PowerSetBenchmark.powSetRecursive          4  avgt    3        0.191 ±       0.087  us/op
PowerSetBenchmark.powSetRecursive          5  avgt    3        0.400 ±       0.071  us/op
PowerSetBenchmark.powSetRecursive          9  avgt    3        7.283 ±       0.500  us/op
PowerSetBenchmark.powSetRecursive         10  avgt    3       20.408 ±      33.346  us/op
PowerSetBenchmark.powSetRecursive         11  avgt    3       57.855 ±      15.787  us/op
PowerSetBenchmark.powSetRecursive         20  avgt    3    82136.368 ±   75290.816  us/op
PowerSetBenchmark.powSetRecursive         26  avgt    3  7995903.683 ± 2029323.013  us/op
```
&nbsp;&nbsp; As you can notice from benchmark summary binary implementation is faster with `n <= 10`, but with `n=11` recursive implementation becomes faster.  
&nbsp;&nbsp; For me it's pretty unexpected result which I cannot explain at the moment. So much the better, another interesting topic to explore is put to the piggy-bank :-) See you!