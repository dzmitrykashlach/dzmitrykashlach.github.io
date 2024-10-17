---
layout: post
title:  "Algorithmic games: shortest path"
date:   2023-07-31 00:42:07 +0300
categories: kotlin
---
&nbsp;&nbsp; Today I want to introduce my variant of solution for [`Shortest Path to Get All Keys` problem](https://leetcode.com/problems/shortest-path-to-get-all-keys/), which is based on [another implementation](http://anothercasualcoder.blogspot.com/2018/12/shortest-path-to-get-all-keys-hard.html). So, [here are my improvements](https://github.com/dzmitrykashlach/algorithms-storehouse/blob/9b8a32ee952b8f2ab0cb9fb7d42b683261c1faa9/impl/src/main/kotlin/com/algorithms/storehouse/arrays/shortpathkeys/ShortTestPathAllKeysBFS.kt).  
&nbsp;&nbsp; Algorithm is based on [`BFS (Breadth-First-Search)`](https://en.wikipedia.org/wiki/Breadth-first_search). It uses [`PathState`](https://github.com/dzmitrykashlach/algorithms-storehouse/blob/9b8a32ee952b8f2ab0cb9fb7d42b683261c1faa9/impl/src/main/kotlin/com/algorithms/storehouse/arrays/shortpathkeys/ShortTestPathAllKeysBFS.kt#L85C16-L85C19) instance for keeping actual traversal state.  
&nbsp;&nbsp; The main trouble with the original implementation was that although it works pretty well, it's impossible to track the whole path step-by-step, which makes understanding logic very difficult.  
&nbsp;&nbsp; Besides cosmetic syntax changes related to migrating code to `Kotlin`, I've made 3 logic updates:  
* [`val moves: LinkedList<Pair<Int, Int>>`](https://github.com/dzmitrykashlach/algorithms-storehouse/blob/9b8a32ee952b8f2ab0cb9fb7d42b683261c1faa9/impl/src/main/kotlin/com/algorithms/storehouse/arrays/shortpathkeys/ShortTestPathAllKeysBFS.kt#L87)  
&nbsp;&nbsp; As mentioned, original implementation didn't have a mechanism of tracking path step by step, so in some complex scenarios like [`getPathTest_4keys_free_ride_center`](https://github.com/dzmitrykashlach/algorithms-storehouse/blob/572472a120a470ce6c7b3a9fe5be7284be08accc/impl/src/test/kotlin/arrays/shortpathkeys/ShortTestPathAllKeysBFSTest.kt#L61) it were cases when some piece of path was not included and therefore total amount of steps was wrong. This fix provides exact chain of steps, e.g. for any scenario it's possible to track traversing logic.
* [`private var centralKeyStore: Set<Char> = mutableSetOf()`](https://github.com/dzmitrykashlach/algorithms-storehouse/blob/9b8a32ee952b8f2ab0cb9fb7d42b683261c1faa9/impl/src/main/kotlin/com/algorithms/storehouse/arrays/shortpathkeys/ShortTestPathAllKeysBFS.kt#L24)  
&nbsp;&nbsp; This element is needed for keeping all found keys in one place, so that they were not distributed in different [`PathState`](https://github.com/dzmitrykashlach/algorithms-storehouse/blob/9b8a32ee952b8f2ab0cb9fb7d42b683261c1faa9/impl/src/main/kotlin/com/algorithms/storehouse/arrays/shortpathkeys/ShortTestPathAllKeysBFS.kt#L85C16-L85C19) instances during traversal.
* [`queue.clear()`](https://github.com/dzmitrykashlach/algorithms-storehouse/blob/9b8a32ee952b8f2ab0cb9fb7d42b683261c1faa9/impl/src/main/kotlin/com/algorithms/storehouse/arrays/shortpathkeys/ShortTestPathAllKeysBFS.kt#L74)  
&nbsp;&nbsp; [`val queue = ArrayDeque<PathState>()`](https://github.com/dzmitrykashlach/algorithms-storehouse/blob/9b8a32ee952b8f2ab0cb9fb7d42b683261c1faa9/impl/src/main/kotlin/com/algorithms/storehouse/arrays/shortpathkeys/ShortTestPathAllKeysBFS.kt#L37) is the main element in `BFS`. In this particular task there were cases, when key was found, but because of other `PathState` instances in queue, traversing was continued from another cell, which is, obviously, wrong. Clearing queue after finding a key and adding it to `centralKeyStore` fixes this issue.

&nbsp;&nbsp; Overall time complexity will be `O(n x m)`, where `n` & `m` - size of grid.  
&nbsp;&nbsp; Although "shortest path" is stated in title, I think that in many cases this approach won't find the shortest path, because this algorithm works in greedy manner, that means that in some cases there can be more with less amount of steps. So, for more optimal way we need to scan the whole grid and use something similar to [`Bellman-Ford algorithm`](https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm), which makes several traversals, each time getting closer to optimal solution.

&nbsp;&nbsp; Hope, it was interesting and helpful, [test cases are here](https://github.com/dzmitrykashlach/algorithms-storehouse/blob/572472a120a470ce6c7b3a9fe5be7284be08accc/impl/src/test/kotlin/arrays/shortpathkeys/ShortTestPathAllKeysBFSTest.kt). See you! :-)



