from config import app, api
from models import Post, Comment
from flask_restful import Resource
from sqlalchemy import func;

# create routes here:
#started at 2:32 AM began testing at 2:58 AM by 3:13 AM 3 pass 3:25 4 pass 4:12 AM all pass

# Challenge 1
# Create a GET route that goes to /api/sorted_posts.
#This route should return as json all the posts alphabetized by title.

class SortedPosts(Resource):
  def get(self):
    apsts = Post.query.order_by(Post.title).all();
    apstdicts = [pst.to_dict() for pst in apsts];
    return apstdicts, 200;

api.add_resource(SortedPosts, "/api/sorted_posts");

# Challenge 2
# Create a GET route that goes to /api/posts_by_author/<author_name>.
#This route should return as json the post by the author's name.
#For example: /api/posts_by_author/sara would return all post that belong to sara.

class PostsByAuthor(Resource):
  def get(self, author_name):
    print(author_name);
    print(Post.query.all());
    #apsts = Post.query.filter_by(author=author_name).all();
    apsts = Post.query.all();
    retapsts = [pst.to_dict() for pst in apsts if pst.author.lower() == author_name.lower()];
    return retapsts, 200;

api.add_resource(PostsByAuthor, "/api/posts_by_author/<author_name>");

# Challenge 3
# Create a GET route that goes to /api/search_posts/<title>.
#This route should return as json all the posts that include the title.
#Capitalization shouldn't matter. So if you were to use this route like /api/search_posts/frog.
#It would give back all post that include frog in the title.

class PostsWithTitle(Resource):
  def get(self, title):
    apsts = Post.query.all();
    retpsts = [];
    for pst in apsts:
      #print(f"title = {title}");
      #print(f"lwrtitle = {title.lower()}");
      #print(f"pst.title = {pst.title}");
      if (title in pst.title or title.lower() in pst.title.lower()):
        retpsts.append(pst);
    retpstdicts = [pst.to_dict() for pst in retpsts];
    return retpstdicts, 200;
  
api.add_resource(PostsWithTitle, "/api/search_posts/<title>");

# Challenge 4
# Create a GET route that goes to /api/posts_ordered_by_comments.
#This route should return as json the posts ordered by how many comments
#the post contains in descendeding order. So the post with the most comments would show
#first all the way to the post with the least showing last.

class PostsByComments(Resource):
  def get(self):
    #apsts = Post.query.order_by(func.count(Post.comments).desc()).all();
    #apstdicts = [pst.to_dict() for pst in apsts];
    #return apstdicts, 200;
    apsts = Post.query.all();
    #number of comments for each post: len(pst.comments)
    #1, 1, 4, 7, 2, 6, 8
    #we need to sort it and we need to know how many has the same number of comments
    #if it matches the number
    #go up to the maximum one
    #if not included skip it
    numcmts = [len(pst.comments) for pst in apsts];
    mxcmnts = max(numcmts);
    retlist = [apsts[x] for i in range(mxcmnts + 1) for x in range(len(numcmts)) if (numcmts[x] == i)]
    revretlist = [retlist[len(retlist) - i - 1] for i in range(len(retlist))];
    
    print(retlist);
    for item in retlist:
      print(len(item.comments));
    #revretlist = reversed(retlist);
    print(revretlist);
    for item in revretlist:
      print(len(item.comments));
    #print(revretlist);
    revlistdicts = [x.to_dict() for x in revretlist];
    print(revlistdicts);
    return revlistdicts, 200;
    
  
api.add_resource(PostsByComments, "/api/posts_ordered_by_comments");

# Challenge 5
# Create a GET route that goes to /api/most_popular_commenter.
#This route should return as json a dictionary like { commenter: "Bob" } of the commenter
#that's made the most comments. Since commenter isn't a model, think of how you can
#count the comments that has the same commenter name.

class MostPopularCommentor(Resource):
  def get(self):
    cmnts = Comment.query.all();
    cmntrs = [cmnt.commenter for cmnt in cmnts];
    mycnts = [cmntrs.count(cnmntr) for cnmntr in cmntrs];
    mxc = max(mycnts);
    print(mxc);
    for i in range(len(mycnts)):
      if (mycnts[i] == mxc):
        cmntrnm = cmntrs[i];
        break;
    return {"commenter": cmntrnm}, 200;
  
api.add_resource(MostPopularCommentor, "/api/most_popular_commenter");

if __name__ == "__main__":
  app.run(port=5555, debug=True)