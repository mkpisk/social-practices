%%DOMAIN
sp(helpwithcup).
actor(pepper).
actor(patient).
purpose(humanholdscup).
objects(table).
objects(cup).
objects(fruit).
location(room).
ison(table, cup).
ison(table, fruit).
moves(pepper).
moves(patient).

%%LOCATION
haslocation(room, X):-
objects(X);
actor(X), X \= 'patient'.
haslocation(room, Y):-
detect(X, Y, identify).

%%CONVERSATION
speaks(X, Y):-
actor(X),
actor(Y), X \= Y.
listens(X, Y):-
speaks(Y, X).
conversation(X,Y):-
speaks(X,Y),
speaks(Y,X).
action(X):-
moves(X).

%%RULEGENERAL
lookat(X, Y):-
conversation(X,Y).
healthsupport(X, takesmed):-
actor(X), X = 'patient'.

%%SPEECHGENERAL
speech(X, Y, speakloud):-
speaks(X,Y),
actor(Y), Y = 'patient'.
speech(X, Y, speaklowtone):-
speaks(X,Y),
actor(Y), Y = 'patient'.
speech(X, Y, speakslow):-
speaks(X,Y),
actor(Y), Y = 'patient'.

%%LISTENGENERAL
listen(X, Y, givetime):-
listens(X,Y).
listen(X, Y, understand):-
listens(X,Y).
listen(X, Y, askagainifnotunderstood):-
listens(X,Y).
listen(X, Y, humantalks):-
speaks(Y,X), Y \= 'pepper'.

gesture(X, Y, showattention):-
listens(X,Y), X = 'pepper'.

%%DETECT
detect(X, Y, identify):-
%%haslocation(room, X),
lookat(X,Y), X = 'pepper'.
detect(X, Y, lookaround):-
%%haslocation(room, X),
No lookat(X,Y), X = 'pepper'.
detecthuman(X, turntosound).

%%IAMHERE
says(X, Y, sayimhere):-
haslocation(room, X),
actor(X),
detect(X, Y, identify), 
lookat(X,Y),
speech(X, Y, speakloud),
speech(X, Y, speakslow),
speech(X, Y, speaklowtone), X = 'pepper', X \= Y. 

gesture(X, Y, showhandsup):-
haslocation(room, X),
actor(X),
detect(X, Y, identify),
lookat(X,Y), X = 'pepper', X \= Y. 

%%GREET
says(X, Y, saygreeting):-
haslocation(room, X),
actor(X),
lookat(X,Y),
speech(X, Y, speakloud),
speech(X, Y, speakslow),
speech(X, Y, speaklowtone), X = 'pepper', X \= Y. 

gesture(X, Y, showhappy):-
haslocation(room, X),
actor(X),
lookat(X, Y), X = 'pepper', X \= Y. 

%%greet(X, Y, humansawpepper).
%%greet(X, Y, humangreeted).

%%HOWCANIHELP
says(X, Y, sayhowcanihelp):-
haslocation(room, X),
actor(X),
service(Y, X, needhelp),
lookat(X, Y),
speech(X, Y, speakloud),
speech(X, Y, speakslow),
speech(X, Y, speaklowtone), X = 'pepper', X \= Y. 

gesture(X, Y, showquestion):-
haslocation(room, X),
actor(X),
service(Y, X, needhelp),
lookat(X, Y), X = 'pepper', X \= Y. 

%hcih(X, Y, humangreeted).
%hcih(X, Y, humanneedshelp).

%%CHECKMEDICATION
says(X, Y, saycheckmed):-
haslocation(room, X),
actor(X),
service(Y, X, needcup),
healthsupport(Y, takesmed),
lookat(X, Y),
speech(X, Y, speakloud),
speech(X, Y, speakslow),
speech(X, Y, speaklowtone), X = 'pepper', X \= Y. 

gesture(X, Y, showexplain):-
haslocation(room, X),
actor(X),
service(Y, X, needcup),
healthsupport(Y, takesmed),
lookat(X, Y), X = 'pepper', X \= Y. 
%%medcheck(X, Y, humanaskedforcup).
%%medcheck(X, Y, medcheckrequired).

%%SERVICES
service(Y, X, needhelp):-
actor(X), X = 'pepper',
says(Y, X, needhelp).
%%Y = 'patient'.

service(Y, X, needcup):-
actor(X), X = 'pepper',
actor(Y),
says(Y, X, needcup).

%%HUMANACTIONS
says(Y, X, needhelp):-
actor(X), actor(Y), X = 'pepper', X \= Y,
haslocation(room, X),
haslocation(room, Y).

says(Y, X, needcup):-
actor(X), actor(Y), X = 'pepper', X \= Y,
haslocation(room, X),
haslocation(room, Y).
