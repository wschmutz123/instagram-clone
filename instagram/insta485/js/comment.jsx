import React from 'react';
import PropTypes from 'prop-types';

class Comment extends React.Component {
/* Display commentList
*/

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { commentInput: '', commentList: [] };
    this.handleNewComment = this.handleNewComment.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;
    // console.log(`comment url ${url}`);

    // Call REST API to get the post's information
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((commentRes) => {
        // console.log(`comment Response:${commentRes.commentList}`);
        this.setState({
          commentList: commentRes.comments,
        });
      })
      .catch((error) => console.log(error));
  }

  handleChange(event) {
    // console.log(`handling change ${event.target.value}`);
    this.setState({ commentInput: event.target.value });
  }

  handleNewComment(event) {
    event.preventDefault();
    const { url } = this.props;
    const { commentInput } = this.state;
    // console.log(`comment input is ${commentInput}`);
    fetch(url, {
      credentials: 'same-origin',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: commentInput,
        // owner: commnetInput.owner
      }),
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((commentRes) => {
        this.setState((addComment) => ({
          commentInput: '',
          commentList: addComment.commentList.concat(commentRes),
        }));
        // this.componentDidMount();
      })
      .catch((error) => console.log(error));
  }

  render() {
    // Should auto render, not sure if i need to handle commentInput more
    const { commentInput, commentList } = this.state;
    return (
      <div>
        <div>
          {commentList.map((comment) => (
            <Comments commentList={comment} key={comment.commentid} />
          ))}
        </div>
        <form className="comment-form" onSubmit={this.handleNewComment}>
          <input type="text" value={commentInput} onChange={this.handleChange} />
        </form>
      </div>
    );
  }
}

function Comments(commentL) {
  const { commentList } = commentL;
  // console.log(commentList);
  // console.log('comment list ', commentList);
  const commentOwner = (
    <p>
      <a
        href={commentList.owner_show_url}
        style={{
          color: 'black',
          textDecoration: 'none',
          fontWeight: 'bold',
        }}
      >
        {commentList.owner}
      </a>
      &nbsp;
      <span>
        {commentList.text}
      </span>
    </p>
  );
  return (
    <div>
      {commentOwner}
    </div>
  );
}

Comment.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Comment;
