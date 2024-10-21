import React from 'react';
import PropTypes from 'prop-types';
import InfiniteScroll from 'react-infinite-scroll-component';
import Post from './post';

class Feed extends React.Component {
  /* Display number of image and post owner of a single post
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { vecPosts: [], next: '', hasMoreitems: true };
  }

  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;
    // include check for if url  is empty

    // Call REST API to get the post's information
    // turn this into a function
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
      //  debugger
        this.setState({
          vecPosts: data.results,
          next: data.next,
          hasMoreitems: true,
        });
      })
      .catch((error) => console.log(error));
  }

  fetchMoreItems() {
    const { next, vecPosts } = this.state;
    if (next === '') {
      setTimeout(() => {
        this.setState({
          hasMoreitems: false,
        });
      }, 500);
      return;
    }
    setTimeout(() => {
      fetch(next, { credentials: 'same-origin' })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
        //  debugger
          this.setState({
            vecPosts: vecPosts.concat(data.results),
            next: data.next,
            hasMoreitems: true,
          });
        })
        .catch((error) => console.log(error));
    }, 500);
    // a fake async api call like which sends
    // 20 more records in .5 sec
  }

  render() {
    // This line automatically assigns this.state.imgUrl to the const variable imgUrl
    // and this.state.owner to the const variable owner
    const { vecPosts, hasMoreitems } = this.state;
    //  console.log("next:"+next);
    //  console.log(`dataLength:${vecPosts.length}`);
    //  console.log("next:"+next);
    // Render number of post image and post owner
    return (
      <div>
        <InfiniteScroll
          dataLength={vecPosts.length}
          next={() => this.fetchMoreItems()}
          hasMore={hasMoreitems}
          scrollThreshold="100%"
        >
          <div>
            {(() => {
              const values = [];
              for (let index = 0; index < vecPosts.length; index += 1) {
                values.push(<Post
                  url={vecPosts[index].url}
                  key={vecPosts[index].url}
                />);
              }
              return values;
            })()}
          </div>
        </InfiniteScroll>
      </div>

    );
  }
}

Feed.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Feed;
