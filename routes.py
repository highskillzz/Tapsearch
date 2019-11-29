from io import StringIO

from flask import *


from invertedindexer import InvertedIndex, Database


admin = Blueprint('admin', __name__)

db = Database()
invertedIndex = InvertedIndex(db)


@admin.route('/', methods=['GET'])
def starter():
    return make_response("Recieved the correct response", 200)


# The code below can be better written by adding map to the split and then indexing it directly
# instead of putting it in again docs variable

@admin.route('/addnewdoc', methods=['POST'])
def addNewDoc():
    doc = request.form["doc"]
    if doc:
        docs = []
        doc = doc.replace('\r', '').split('\n\n')
        for doc in doc:
            docs.append(doc)
        for eachDoc in docs:
            invertedIndex.index_document(eachDoc)
    return make_response("Recieved the correct response", 200)


@admin.route('/search/<query>', methods=['POST'])
def results(query):
    searchResults = []
    query = query.lower()
    result = invertedIndex.lookup_query(query)
    print(result)
    if result[query] == None:
        return make_response('No documents match your search', 200)
    else:
        for term in result.keys():
            for appearance in result[term]:
                doc = db.get(appearance.docId)
                searchResults.append(doc)
        searchResults = list(set(searchResults))
        return make_response(jsonify(searchResults), 200)


@admin.route('/removeall', methods=['GET'])
def removeAll():
    db.db = dict()
    invertedIndex.index = dict()
    invertedIndex.db = db
    invertedIndex.uniqueID = 0
    return make_response("Removed all the documents", 200)


@admin.route('/viewall', methods=['GET'])
def viewAll():
    searchResults = []
    for _, v in db.db.items():
        searchResults.append(v)
    searchResults = list(set(searchResults))
    return make_response(jsonify(searchResults), 200)


# @admin.route('/load-new-doc', methods=['POST', 'GET'])
# def loadNewDocPage():
#     newDocForm = NewDocForm()
#     if newDocForm.validate_on_submit():
#         document = newDocForm.document.data
#         if document:
#             documents = []
#             document = document.replace('\r', '').split('\n\n')
    # for document in document:
    #     documents.append(document)
    # for eachDocument in documents:
    #     invertedIndex.index_document(eachDocument)
#             return redirect(url_for('admin.landingPage'))
#     return render_template('load-new-doc.html', form=newDocForm)


# @admin.route('/<query>/search-results', methods=['POST', 'GET'])
# def resultPage(query):
#     searchResults = []
#     result = invertedIndex.lookup_query(query)
#     if result[0]:
#         for term in result[1].keys():
#             for appearance in result[1][term]:
#                 document = db.get(appearance.docId)
#                 searchResults.append(document)
#     else:
#         print('No documents match your search')
#     searchResults = list(set(searchResults))
#     if searchResults:
#         return render_template('search-results.html', searchResults=searchResults)
#     else:
#         return render_template('no-docs-found.html')


# @admin.route('/view-all-docs', methods=['POST', 'GET'])
# def viewAllDocs():
    # searchResults = []
    # for _, v in db.db.items():
    #     searchResults.append(v)
    # searchResults = list(set(searchResults))
#     if searchResults:
#         return render_template('view-all-docs.html', searchResults=searchResults)
#     else:
#         return render_template('no-docs-found.html')


# @admin.route('/erase-all-docs', methods=['POST', 'GET'])
# def eraseAllDocs():
#     db.db = dict()
#     invertedIndex.index = dict()
#     invertedIndex.db = db
#     invertedIndex.uniqueID = 0
#     return render_template('erase-all-docs.html')
