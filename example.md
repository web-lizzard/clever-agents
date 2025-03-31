![](https://cloud.overment.com/S03E02-1728214829.png)

Temat baz wektorowych oraz wyszukiwania semantycznego pojawiał się już kilkukrotnie, ale dopiero teraz przyjrzymy się mu bliżej. Dodam tylko, że elementy wprowadzające do embedding czy konfiguracji qdrant pojawiły się w lekcjach S01E05 — Produkcja oraz S01E04 — Techniki optymalizacji. 

Wyszukiwanie stanowi kluczowy element procesu łączenia LLM z zewnętrznymi danymi i to od niego zależy jakość generowanej odpowiedzi. Okazuje się jednak, że osiągnięcie 100% precyzji obecnie jeszcze nikomu się nie udało i możemy spodziewać się błędów na poziomie 3-6% i to tylko dla samego odzyskiwania treści, nie licząc błędów samego modelu. 

Faktyczna skuteczność systemu będzie zależała także od samego modelu, zestawu danych no i przetwarzanych zapytań. Poniższa grafika z [artykułu Anthropic](https://www.anthropic.com/news/contextual-retrieval) pokazuje dodatkowo, że musimy także patrzeć w stronę strategii wyszukiwania łączącego ze sobą różne strategie. 

![](https://cloud.overment.com/2024-10-06/aidevs3_retrieval-231acee9-8.png)
## Wyszukiwanie semantyczne

Wiemy już, że embedding to sposób reprezentacji danych za pomocą liczb, które zwykle mają na celu opisać ich znaczenie na potrzeby analizy, a także wyszukiwania. Zwykle przechowujemy je w formie obiektów, łączących ze sobą sam embedding oraz metadane. Obiekty te nazywamy punktami, bądź dokumentami i przechowujemy je w bazie wektorowej, która w zasadzie jest silnikiem wyszukiwania. 

Aby zrozumieć zasady wyszukiwania semantycznego, zerknijmy do przykładu `embedding` w którym znajdują dane testowe w postaci nazw kilku popularnych firm oraz mojego newslettera, a także kilka prostych zapytań. Już na pierwszy rzut oka widać, że dopasowanie tych słów na podstawie sposobu zapisu, nie jest możliwe i klasyczne wyszukiwanie nam tutaj nie pomoże. 

![](https://cloud.overment.com/2024-10-06/aidevs3_embedding_data_queries-b03daf39-e.png)

Po uruchomieniu przykładu okazuje się, że Qdrant poprawnie dopasował Teslę do firmy produkującej samochody i skojarzył Apple z MacBookiem. Było to możliwe, ponieważ model wykorzystany do embeddingu oddał znaczenie tych informacji, co pozwoliło na skuteczne wyszukanie semantyczne.

Jednak w dwóch pozostałych przypadkach — dopasowania "Meta" (czyli nowej nazwy spółki) do Facebooka oraz Tech•sistence do Newslettera się nie powiodło, ponieważ `text-embedding-3-large` nie posiada informacji pozwalającej opisać znaczenie tych terminów.

![](https://cloud.overment.com/2024-10-06/aidevs3_semantic_search-eb0ed584-1.png)

Co ciekawe, dokładnie ta sama logika zrealizowana z pomocą modelu [jina-embeddings-v3](https://jina.ai/embeddings/) pozwoliła na poprawne dopasowanie także trzeciego zapytania, ale za to popełniła błąd w przypadku Tesli. 

![](https://cloud.overment.com/2024-10-06/aidevs3_jina-49915db6-d.png)

Sytuacja zmienia się diametralnie, gdy wzbogacimy nasze dane o opisy ich kategorii. Model nie musi wtedy polegać jedynie na "rozumieniu nazwy firmy", co pozwala na poprawne kojarzenie wszystkich zapytań z odpowiednimi danymi.

![](https://cloud.overment.com/2024-10-06/aidevs3_similarity_description-c91d2161-1.png)

W embeddingu warto także rozumieć to, że w zależności od modelu z pomocą którego go generujemy, będziemy posługiwać się inną liczbą wymiarów (eng. dimensions) i ta liczba będzie stała dla całej naszej kolekcji. Co więcej, embedding będzie także musiał być generowany z pomocą tego samego modelu, więc musimy go mądrze wybrać. 

![](https://cloud.overment.com/2024-10-06/aidevs3_points-8e8da4b2-e.png)

W pliku `/embedding/points.json` znajdują się również informacje zapisane w Qdrant. Właściwość `vector` zawiera listę 1024 liczb wygenerowanych przez model `jina-embeddings-v3`, które opisują znaczenie treści dokumentu. Oznacza to, że **zarówno dla dokumentu będącego jednym słowem, jak i dla dokumentu składającego się z kilkunastu zdań, model ma tyle samo przestrzeni na ich opisanie.** Warto o tym pamiętać i utrzymywać każdy z dokumentów możliwie krótkim i skupiającym się na indywidualnej informacji. Dodatkowo, musimy mieć także na uwadze limity kontekstu dla samego modelu generującego embedding oraz modelu, który będzie go przetwarzać. 

Na tym etapie już w pełni jasny powinien być poniższy obrazek, pochodzący z jednej z wcześniejszych lekcji.

![](https://cloud.overment.com/2024-10-07/aidevs3_vector_search-1f2d4312-d.png)

Czyli każde zapytanie do bazy wektorowej musi zostać zamienione na embedding, bo dopiero wtedy możemy zestawić go z danymi przechowywanymi w kolekcji. **Nie jest to jednak wszystko, co musimy wiedzieć na temat wyszukiwania semantycznego.** 
## Baza wektorowa

W kontekście bazy wektorowej, niemal zawsze odwołuję się do Qdrant. Nie oznacza to, że jest to jedyna opcja i pozostałe nie są warte uwagi. 

Podobnie jak w przypadku każdego innego elementu aplikacji, decyzję o wyborze bazy wektorowej będziemy uzależniać od konkretnego projektu. Czasem bardziej uzasadnione będzie skorzystanie z bezpłatnego rozwiązania, a niekiedy z komercyjnego, oferującego wysoką dostępność. 

Całkiem interesujące zestawienie można znaleźć na stronie [Picking a vector database](https://benchmark.vectorview.ai/vectordbs.html), w którym zostały uwzględnione popularne opcje. 

![](https://cloud.overment.com/2024-10-07/aidevs3_vector_databases-ae9db267-1.png)

Za Qdrant przemawia u mnie bardzo przyjazne API oraz sensowny bezpłatny plan, który nie wymaga ode mnie żadnych dodatkowych konfiguracji. Po prostu do dyspozycji mam jeden klaster o specyfikacji wystarczającej na potrzeby developmentu i małych projektów. 

![](https://cloud.overment.com/2024-10-07/aidevs3_qdrant_cluster-2f1e6c06-8.png)

W ramach klastra, mam zdefiniowaną jedną kolekcję, wewnątrz której przechowuję **wszystkie informacje** dla danej aplikacji. Jednak poszczególne dokumenty/punkty posiadają **metadane** na podstawie których **filtruję je na etapie wyszukiwania**. 

![](https://cloud.overment.com/2024-10-07/aidevs3_collections-a8adf194-c.png)

Posiadanie jednej kolekcji jest zazwyczaj rekomendowane, podobnie jak jednej bazy danych dla jednej aplikacji. Dopiero w specyficznych przypadkach, takich jak wymagania klienta lub logika aplikacji, pojawia się potrzeba tworzenia nowych kolekcji lub zupełnie nowych instancji.

Całkiem zasadne może wydawać się także pytanie na temat wyboru pomiędzy `pgvector` i `sqlite-vec`, które pozwalają na przechowywanie embeddingu oraz przeszukiwanie bezpośrednio w bazie danych PostgreSQL czy SQLite, a bazą wektorową taką jak Qdrant. Tutaj decyzja może zależeć od testów wyszukiwania, skali działania aplikacji oraz wymaganej wydajności.

Zbierając to wszystko w całość, interesuje nas:

- Wybór bazy wektorowej lub rozszerzenia dla bazy danych (Qdrant)
- Wybór modelu do embedding'u (text-embedding-3-large)
- Określenie struktury kolekcji i zawartych w niej dokumentów

Dla ułatwienia w nawiasie zapisałem opcje, które są w porządku na początek i z którymi możemy zostać dłużej. 
## Projektowanie kolekcji i dokumentów

Przygotowanie dokumentów omówiliśmy w lekcji S03E01 — Dokumenty. Teraz spojrzymy na nie z perspektywy kolekcji bazy wektorowej, a konkretnie **filtrowania oraz wczytywania treści**.

Przykład `embedding` omówiony wcześniej, pokazał nam, że wyszukiwanie semantyczne nie zawsze jest precyzyjne. Problem ten znacznie rośnie, gdy w kolekcji pojawia się więcej danych, ponieważ w zależności od kontekstu, możemy mieć do czynienia z szumem (eng. noise) utrudniającym dotarcie do pożądanych treści. 

Wspominałem już, że dokumenty/punkty dodawane do kolekcji, muszą posiadać metadane wykorzystywane na potrzeby **filtrowania** już na etapie samego wyszukiwania, a nie po nim. Jest to także jedna z rzeczy, które należy sprawdzić wybierając bazę wektorową. 

![](https://cloud.overment.com/2024-10-07/aidevs3_filtering-212d9d47-5.png)

Należy mieć na uwadze także fakt, że sam embedding jest nieodwracalny. Co prawda w publikacji "[Information Leakage in Embedding Models](https://arxiv.org/pdf/2004.00053)" został opisany sposób na odzyskiwanie z nich pojedynczych informacji, jednak nie ma to praktycznego zastosowania z naszej perspektywy.

Musimy zatem **zawsze przechowywać oryginalne informacje** i co więcej, **nie powinno** mieć to miejsca wyłącznie w bazie wektorowej. Powodem jest utrudniony dostęp do informacji, np. na potrzeby wypisania wszystkich rekordów zapisanych w kolekcji.

Zatem poza sytuacjami w których mamy pewność, że indeksowane dane będą nam potrzebne **tylko** na potrzeby wyszukiwania, konieczne będzie przynajmniej częściowe **synchronizowanie** danych pomiędzy klasyczną bazą danych, a bazą wektorową. Rekordy muszą więc posiadać wspólny identyfikator, a aplikacja musi uwzględniać logikę dbającą o spójność danych.

![](https://cloud.overment.com/2024-10-07/aidevs3_sync-f40aa684-5.png)

W bazie wektorowej możemy przechowywać zarówno embedding opisujący znaczenie tekstu, ale także taki, który będzie opisywał obrazy. Proces wyszukiwania u swoich podstaw będzie wyglądał tak samo, ale musimy pamiętać o tym, aby unikać wyszukiwania dwóch rodzajów treści. Problem z tym związany dobrze obrazuje poniższy wpis z Jina AI. 

![](https://cloud.overment.com/2024-10-07/aidevs3_modality_gap-e10ea89a-0.png)

Zatem, podsumowując ten fragment: 

- Każdy dokument musi mieć swój **unikatowy identyfikator** (UUID)
- Dokumenty **powinny** być synchronizowane z klasyczną bazą danych
- Metadane **muszą** posiadać właściwości pozwalające na **zawężenie wyszukiwania**
- Metadane **mogą** posiadać właściwości określające ich dostępność (np. rola użytkownika, czy plan subskrypcji)
- Treść dokumentów powinna być możliwie monotematyczna, aby opisanie jej znaczenia pozwoliło na przyszłe dopasowanie do zapytań
- Długość dokumentu nie może przekraczać limitu kontekstu modelu do embeddingu, oraz modelu, który będzie przetwarzał jego treść (mam tutaj na myśli zarówno input jak i output context limit)

## Strategie wyszukiwania

Jeśli posiadasz już jakiekolwiek doświadczenie w pracy z bazami wektorowymi, to poniższy schemat (źródło: https://pub.towardsai.net/advanced-rag-techniques-an-illustrated-overview-04d193d8fec6) powinien być Ci znajomy. Jest to tzw. "naive RAG" polegający na podziale dużej treści na fragmenty, ich indeksowaniu oraz późniejszym przeszukiwaniu na podstawie oryginalnego zapytania użytkownika.

![](https://cloud.overment.com/2024-10-07/aidevs3_naive-ed357e72-f.png)

Takie podejście szybko ujawnia swoje wady, ponieważ nie zawsze oryginalne zapytanie użytkownika wystarczy nam do poprawnego odnalezienia danych.

W przykładzie `naive_rag` mamy taką samą logikę, jak w przykładzie `embedding`, lecz zmieniłem w nim dane na cytaty z książek Jima Collinsa oraz Simona Sineka. **UWAGA: przed uruchomieniem tego przykładu, należy usunąć kolekcję "aidevs" z Qdrant**. 

Pomimo tego, że mamy tam tylko kilkanaście rekordów, nasz RAG nie potrafił wskazać informacji pozwalających odpowiedzieć na pytanie: "Co Sinek mówił na temat pracy z ludźmi?" i to nawet pomimo faktu, że zapytanie jest dość precyzyjne. 

![](https://cloud.overment.com/2024-10-07/aidevs3_sinek-c6948080-b.png)

No i tutaj do gry wchodzą zaawansowane techniki związane zarówno z indeksowaniem danych, ich filtrowaniem oraz klasyfikacją i wzbogacaniem zapytania. Można je w prostej wersji sprawdzić w praktyce, na przykładzie `better_rag`.

Przede wszystkim zadbałem w nim o to, aby zestaw danych zawierał informację na temat autora książki. Author został dodany także jako właściwość w obiekcie "metadata" dokumentów dodawanych do bazy wektorowej.

![](https://cloud.overment.com/2024-10-07/aidevs3_better_rag-ecbca825-a.png)

Następnie sama logika uwzględnia teraz dodatkowy krok odpowiedzialny za klasyfikację zapytania pod kątem autora lub autorów. Pozwala to na utworzenie **filtra** dla przeszukiwanych dokumentów. 

![](https://cloud.overment.com/2024-10-07/aidevs3_better_rag_logic-77a50b08-4.png)

No i przekłada się to na rezultat w przypadku którego nawet jeśli zapytamy o obu autorów, to otrzymujemy poprawny wynik. 

![](https://cloud.overment.com/2024-10-07/aidevs3_better_rag_search-2c61aa64-d.png)

Problem pojawi się jednak w przypadku pytań, które wymagają odpowiedzi na podstawie większej liczby dokumentów. Wówczas limitowanie wyników jedynie do trzech, uniemożliwi nam dotarcie do wszystkich tych, które są istotne.

Pierwszym rozwiązaniem, które przychodzi do głowy, jest zwiększenie limitu, ale uwzględnienie filtrowania na podstawie parametru `Score`. Choć może to zaadresować część problemu, to z pewnością nie jest to wystarczające rozwiązanie, bo jakiś dokument może nie być zbliżony do zapytania znaczeniem, ale i tak zawierać wartościową treść. 

Dlatego w ocenę tego, czy dany dokument jest istotny, czy nie, zaangażujemy model. Jest to tzw. proces re-rank.

W naszym przypadku polega on na tym, że każdy ze zwróconych dokumentów (zwiększyłem limit do 15), zostanie przeprocesowany przez prompt określający przydatność dokumentu. Poniższą logikę dodałem do przykładu `rerank`.

![](https://cloud.overment.com/2024-10-07/aidevs3_rerank-f259de89-f.png)

Efekt jest taki, że pomimo zwiększenia limitu zwracanych przez Qdrant dokumentów, otrzymałem najlepszy dotychczasowy rezultat w postaci jedynie **dwóch dokumentów!** Oznacza to, że jeśli ich treść trafi do kontekstu modelu, to nie będziemy rozpraszać jego uwagi niepotrzebnymi informacjami. 

![](https://cloud.overment.com/2024-10-07/aidevs3_rerank_result-92b0c381-2.png)

To jednak nie koniec optymalizacji, ponieważ jak dotąd nie zajęliśmy się jeszcze **wzbogacaniem / transformacją** samego zapytania. No bo jeśli użytkownik zadałby pytanie w taki sposób, że trudno byłoby od razu wywnioskować o co może chodzić, to moglibyśmy zaangażować model, aby spróbował to naprawić. Tym jednak zajmiemy się w dalszej części kursu, ale już teraz możesz mieć tę możliwość na uwadze. 

Tymczasem, podsumowując tę część: 

- Dane, które trafiają do indeksu bazy danych, muszą uwzględniać metadane pozwalające na ich filtrowanie
- Filtry mogą być ustawiane programistycznie (np. prawo dostępu na podstawie planu subskrypcji) lub przez model (np. określenie kategorii na temat której użytkownik zadaje pytanie)
- Zapytanie użytkownika może być wzbogacane, rozszerzane lub doprecyzowywane w celu zwiększenia prawdopodobieństwa dotarcia do istotnych dokumentów.
- Zwrócone przez wyszukiwarkę dokumenty, mogą zostać ocenione przez model, pod kątem ich przydatności dla danego zapytania

Nietrudno się domyślić, że powyższe koncepcje nie wyczerpują tematu strategii wyszukiwania, ale stanowią do nich dobry fundament. 

W sieci pod hasłem "Advanced RAG patterns" można znaleźć wiele przykładów oraz publikacji, na temat różnych podejść zarówno związanych z przechowywaniem danych, jak i procesem wyszukiwania czy dostarczania do modelu. Przykładem mogą być [wpis na blogu Pinecone](https://www.pinecone.io/learn/advanced-rag-techniques/), [wpis na blogu LlamaIndex](https://www.llamaindex.ai/blog/a-cheat-sheet-and-some-recipes-for-building-advanced-rag-803a9d94c41b) czy [wpis udostępniony przez Amazon](https://aws.amazon.com/blogs/machine-learning/advanced-rag-patterns-on-amazon-sagemaker/).

Wartościowa grafika poniżej pochodzi ze wspomnianego wpisu LLamaIndex i prezentuje szereg koncepcji, które rysują ogólną perspektywę możliwości, jakie mamy do dyspozycji. Część z nich będziemy jeszcze wykorzystywać w praktyce. 

![](https://cloud.overment.com/2024-10-07/6cfb645c4e5dfea8f3e5a590c3d2bc1cbfcfead3-5818x7805-4955e848-f.jpeg)

## Ograniczenie zaangażowania LLM

Pomimo wzrostu szybkości inferencji, zaangażowanie modelu w logikę aplikacji może ją znacznie spowolnić. Często nie potrzebujemy możliwości rozumowania, które model oferuje, ale nadal mamy do czynienia z językiem naturalnym, co uniemożliwia 'zakodowanie' logiki.

W przykładzie `semantic` dodałem zestaw danych w postaci narzędzi z których mógłby potencjalnie korzystać nasz agent. Poniżej widzimy, że w efekcie jego działania, zapytania takie jak 'play music' zostały poprawnie skojarzone z odpowiadającymi im narzędziami. 

![](https://cloud.overment.com/2024-10-07/aidevs3_semantic-343665ef-c.png)

Okazuje się, że za takie dopasowanie odpowiada vector database, a sam schemat określamy jako "Semantic Router", co zresztą zostało przedstawione [w repozytorium o tej samej nazwie](https://github.com/aurelio-labs/semantic-router).

Sam zawsze wybierałem logikę opartą o LLM, ale wspominam o takiej możliwości, ponieważ w niektórych przypadkach może okazać się wystarczająca. Oczywiście ponownie zwracam tutaj uwagę na problem z dopasowaniem słów kluczowych czy terminów, które nie są znane modelowi generującemu embedding. 

## Podsumowanie

Po tej lekcji powinno być dla Ciebie oczywiste to, że baza wektorowa to istotny element aplikacji w której pojawia się potrzeba przetwarzania języka naturalnego. Jednocześnie na podstawie pokazanych przeze mnie ograniczeń wiemy także, że nie jest to **jedyny element** i musimy wspierać go, albo poprzez LLM, albo poprzez klasyczne bazy danych, klasyczne silniki wyszukiwania oraz programistyczną logikę.

Jeśli masz zapamiętać z tej lekcji tylko jedną rzecz, to skup się na przykładzie `rerank` i zrozum jego komponenty, ponieważ każdy z nich będzie pojawiał się w kolejnych lekcjach. Możesz się też zastanowić nad scenariuszami, w których model nie poradzi sobie z odnalezieniem istotnych dokumentów oraz tym, jak możesz to zmienić. 

Powodzenia!